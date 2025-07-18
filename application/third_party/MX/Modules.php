<?php

if ( ! defined('BASEPATH')) {
    exit('No direct script access allowed');
}

defined('EXT') || define('EXT', '.php');

global $CFG;

// get module locations from config settings or use the default module location and offset
if ( ! is_array(Modules::$locations = $CFG->item('modules_locations'))) {
    Modules::$locations = [
        APPPATH . 'modules/' => '../modules/',
    ];
}

// PHP5 spl_autoload
spl_autoload_register('Modules::autoload');

function myEach($arr): array|false
{
    $key    = key($arr);
    $result = ($key === null) ? false : [$key, current($arr), 'key' => $key, 'value' => current($arr)];
    next($arr);

    return $result;
}

/**
 * Modular Extensions - HMVC.
 *
 * Adapted from the CodeIgniter Core Classes
 *
 * @see    http://codeigniter.com
 *
 * Description:
 * This library provides functions to load and instantiate controllers
 * and module controllers allowing use of modules and the HMVC design pattern.
 *
 * Install this file as application/third_party/MX/Modules.php
 *
 * @copyright    Copyright (c) 2015 Wiredesignz
 *
 * @version    5.5
 *
 * Permission is hereby granted, free of charge, to any person obtaining a copy
 * of this software and associated documentation files (the "Software"), to deal
 * in the Software without restriction, including without limitation the rights
 * to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
 * copies of the Software, and to permit persons to whom the Software is
 * furnished to do so, subject to the following conditions:
 *
 * The above copyright notice and this permission notice shall be included in
 * all copies or substantial portions of the Software.
 *
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
 * IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
 * FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
 * AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
 * LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
 * OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
 * THE SOFTWARE.
 **/
#[AllowDynamicProperties]
class Modules
{
    public static $routes;

    public static $registry;

    public static $locations;

    /**
     * Run a module controller method
     * Output from module is buffered and returned.
     **/
    public static function run($module)
    {
        $method = 'index';
        $args   = func_get_args();

        if (($pos = mb_strrpos($module, '/')) != false) {
            $method = mb_substr($module, $pos + 1);
            $module = mb_substr($module, 0, $pos);
        }

        if (($class = self::load($module)) && method_exists($class, $method)) {
            ob_start();
            $output = call_user_func_array([$class, $method], array_slice($args, 1));
            $buffer = ob_get_clean();

            return ($output !== null) ? $output : $buffer;
        }

        log_message('error', sprintf('Module controller failed to run: %s/%s', $module, $method));
    }

    /** Load a module controller **/
    public static function load($module)
    {
        if (is_array($module)) {
            list($module, $params) = @myEach($module);
        } else {
            $params = null;
        }

        // get the requested controller class name
        $alias = $module == null ? '' : mb_strtolower(basename($module));

        // create or return an existing controller from the registry
        if ( ! isset(self::$registry[$alias])) {
            // find the controller
            list($class) = $module == null ? CI::$APP->router->locate([]) : CI::$APP->router->locate(explode('/', $module));

            // controller cannot be located
            if (empty($class)) {
                return;
            }

            // set the module directory
            $path = APPPATH . 'controllers/' . CI::$APP->router->directory;

            // load the controller class
            $class .= CI::$APP->config->item('controller_suffix');
            self::load_file(ucfirst($class), $path);

            // create and register the new controller
            $controller             = ucfirst($class);
            self::$registry[$alias] = new $controller($params);
        }

        return self::$registry[$alias];
    }

    /** Load a module file **/
    public static function load_file($file, string $path, $type = 'other', $result = true)
    {
        $file     = str_replace(EXT, '', $file);
        $location = $path . $file . EXT;

        if ($type === 'other') {
            if (class_exists($file, false)) {
                log_message('debug', 'File already loaded: ' . $location);

                return $result;
            }

            include_once $location;
        } else {
            // load config or language array
            include $location;

            if ( ! isset(${$type}) || ! is_array(${$type})) {
                show_error(sprintf('%s does not contain a valid %s array', $location, $type));
            }

            $result = ${$type};
        }

        log_message('debug', 'File loaded: ' . $location);

        return $result;
    }

    /** Library base class autoload **/
    public static function autoload(string $class)
    {
        // don't autoload CI_ prefixed classes or those using the config subclass_prefix
        if (mb_strstr($class, 'CI_') || mb_strstr($class, config_item('subclass_prefix'))) {
            return;
        }

        // autoload Modular Extensions MX core classes
        if (mb_strstr($class, 'MX_')) {
            if (is_file($location = dirname(__FILE__) . '/' . mb_substr($class, 3) . EXT)) {
                include_once $location;

                return;
            }

            show_error('Failed to load MX core class: ' . $class);
        }

        // autoload core classes
        if (is_file($location = APPPATH . 'core/' . ucfirst($class) . EXT)) {
            include_once $location;

            return;
        }

        // autoload library classes
        if (is_file($location = APPPATH . 'libraries/' . ucfirst($class) . EXT)) {
            include_once $location;

            return;
        }
    }

    /** Parse module routes **/
    public static function parse_routes(string $module, $uri)
    {
        // load the route file
        if ( ! isset(self::$routes[$module]) && list($path) = self::find('routes', $module, 'config/')) {
            $path && self::$routes[$module] = self::load_file('routes', $path, 'route');
        }

        if ( ! isset(self::$routes[$module])) {
            return;
        }

        // parse module routes
        foreach (self::$routes[$module] as $key => $val) {
            $key = str_replace([':any', ':num'], ['.+', '[0-9]+'], $key);

            if (preg_match('#^' . $key . '$#', $uri)) {
                if (str_contains($val, '$') && str_contains($key, '(')) {
                    $val = preg_replace('#^' . $key . '$#', $val, $uri);
                }

                return explode('/', $module . '/' . $val);
            }
        }
    }

    /**
     * Find a file
     * Scans for files located within modules directories.
     * Also scans application directories for models, plugins and views.
     * Generates fatal error if file not found.
     *
     * @return mixed[]
     **/
    public static function find($file, $module, string $base): array
    {
        $segments = explode('/', $file);

        $file     = array_pop($segments);
        $file_ext = (pathinfo($file, PATHINFO_EXTENSION) !== '' && pathinfo($file, PATHINFO_EXTENSION) !== '0') ? $file : $file . EXT;

        $path                       = mb_ltrim(implode('/', $segments) . '/', '/');
        $module ? $modules[$module] = $path : $modules = [];

        if ($segments !== []) {
            $modules[array_shift($segments)] = mb_ltrim(implode('/', $segments) . '/', '/');
        }

        foreach (self::$locations as $location => $offset) {
            foreach ($modules as $module => $subpath) {
                $fullpath = $location . $module . '/' . $base . $subpath;

                if ($base == 'libraries/' || $base == 'models/') {
                    if (is_file($fullpath . ucfirst($file_ext))) {
                        return [$fullpath, ucfirst($file)];
                    }
                } elseif (is_file($fullpath . $file_ext)) {
                    // load non-class files
                    return [$fullpath, $file];
                }
            }
        }

        return [false, $file];
    }
}
