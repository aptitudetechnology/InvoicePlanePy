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
class Mdl_Email_Templates extends Response_Model
{
    public $table = 'ip_email_templates';

    public $primary_key = 'ip_email_templates.email_template_id';

    public function default_select()
    {
        $this->db->select('SQL_CALC_FOUND_ROWS *', false);
    }

    public function default_order_by()
    {
        $this->db->order_by('email_template_title');
    }

    /**
     * @return array
     */
    public function validation_rules()
    {
        return [
            'email_template_title' => [
                'field' => 'email_template_title',
                'label' => trans('title'),
                'rules' => 'required',
            ],
            'email_template_type' => [
                'field' => 'email_template_pdf_quote_template',
                'label' => trans('type'),
            ],
            'email_template_subject' => [
                'field' => 'email_template_subject',
                'label' => trans('subject'),
            ],
            'email_template_from_name' => [
                'field' => 'email_template_from_name',
                'label' => trans('from_name'),
                'rules' => 'trim',
            ],
            'email_template_from_email' => [
                'field' => 'email_template_from_email',
                'label' => trans('from_email'),
            ],
            'email_template_cc' => [
                'field' => 'email_template_cc',
                'label' => trans('cc'),
            ],
            'email_template_bcc' => [
                'field' => 'email_template_bcc',
                'label' => trans('bcc'),
            ],
            'email_template_pdf_template' => [
                'field' => 'email_template_pdf_template',
                'label' => trans('default_pdf_template'),
            ],
            'email_template_body' => [
                'field' => 'email_template_body',
                'label' => trans('body'),
            ],
        ];
    }
}
