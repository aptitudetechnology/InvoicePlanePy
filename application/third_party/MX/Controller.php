<?php

if ( ! defined('BASEPATH')) {
    exit('No direct script access allowed');
}

/** load the CI class for Modular Extensions **/
require dirname(__FILE__) . '/Base.php';

/**
 * Modular Extensions - HMVC.
 *
 * Adapted from the CodeIgniter Core Classes
 *
 * @see    http://codeigniter.com
 *
 * Description:
 * This library replaces the CodeIgniter Controller class
 * and adds features allowing use of modules and the HMVC design pattern.
 *
 * Install this file as application/third_party/MX/Controller.php
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
class MX_Controller
{
    public $load;

    public $autoload = [];

    public function __construct()
    {
        if (CI::$APP->config->item('controller_suffix') == null) {
            $class = str_replace('', '', get_class($this));
        } else {
            $class = str_replace(CI::$APP->config->item('controller_suffix'), '', get_class($this));
        }

        log_message('debug', $class . ' MX_Controller Initialized');
        Modules::$registry[mb_strtolower($class)] = $this;

        // copy a loader instance and initialize
        $this->load = clone load_class('Loader');
        $this->load->initialize($this);

        // autoload module items
        $this->load->_autoloader($this->autoload);
    }

    public function __get($class)
    {
        return CI::$APP->{$class};
    }
}
