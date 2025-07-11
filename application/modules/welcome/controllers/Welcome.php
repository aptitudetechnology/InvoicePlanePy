<?php

if ( ! defined('BASEPATH')) {
    exit('No direct script access allowed');
}

/*
 * InvoicePlane
 *
 * @author      InvoicePlane Developers & Contributors
 * @copyright   Copyright (c) 2012 - 2018 InvoicePlane.com
 * @license     https://invoiceplane.com/license.txt
 * @link        https://invoiceplane.com
 */

#[AllowDynamicProperties]
class Welcome extends CI_Controller
{
    public function index()
    {
        $this->load->model('settings/mdl_settings');
        $this->load->helper(['settings', 'echo', 'url']);
        $this->load->view('welcome');
    }
}
