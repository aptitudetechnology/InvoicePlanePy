<?php

if ( ! defined('BASEPATH')) {
    exit('No direct script access allowed');
}

/*
 * InvoicePlane
 *
 * @author		InvoicePlane Developers & Contributors
 * @copyright	Copyright (c) 2012 - 2018 InvoicePlane.com
 * @license		https://invoiceplane.com/license.txt
 * @link		https://invoiceplane.com
 */

#[AllowDynamicProperties]
class Layout extends MX_Controller
{
    public $view_data = [];

    /**
     * @return $this
     */
    public function buffer(...$args): static
    {
        if (count($args) == 1) {
            foreach ($args[0] as $arg) {
                $key  = $arg[0];
                $view = explode('/', $arg[1]);
                $data = array_merge($arg[2] ?? [], $this->view_data);

                $this->view_data[$key] = $this->load->view($view[0] . '/' . $view[1], $data, true);
            }
        } else {
            $key  = $args[0];
            $view = explode('/', $args[1]);
            $data = array_merge($args[2] ?? [], $this->view_data);

            $this->view_data[$key] = $this->load->view($view[0] . '/' . $view[1], $data, true);
        }

        return $this;
    }

    /**
     * @return $this
     */
    public function set(...$args): static
    {
        if (count($args) == 1) {
            foreach ($args[0] as $key => $value) {
                $this->view_data[$key] = $value;
            }
        } else {
            $this->view_data[$args[0]] = $args[1];
        }

        return $this;
    }

    public function render(string $view = 'layout')
    {
        $this->load->view('layout/' . $view, $this->view_data);
    }

    /**
     * Simple function to load a view directly using the assigned template
     * Does not use buffering or rendering.
     *
     * @param string $view
     * @param array  $data
     */
    public function load_view($view, $data = [])
    {
        $view = explode('/', $view);

        $view = $view[0] . '/' . $view[1] . (isset($view[2]) ? '/' . $view[2] : '');

        $this->load->view($view, $data);
    }
}
