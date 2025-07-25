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
class Mdl_Quote_Tax_Rates extends Response_Model
{
    public $table = 'ip_quote_tax_rates';

    public $primary_key = 'ip_quote_tax_rates.quote_tax_rate_id';

    public function default_select()
    {
        $this->db->select('ip_tax_rates.tax_rate_name AS quote_tax_rate_name');
        $this->db->select('ip_tax_rates.tax_rate_percent AS quote_tax_rate_percent');
        $this->db->select('ip_quote_tax_rates.*');
    }

    public function default_join()
    {
        $this->db->join('ip_tax_rates', 'ip_tax_rates.tax_rate_id = ip_quote_tax_rates.tax_rate_id');
    }

    /**
     * @return void
     */
    public function save($id = null, $db_array = null)
    {
        // Only appliable in legacy calculation - since 1.6.3
        config_item('legacy_calculation') && parent::save($id, $db_array);

        $this->load->model('quotes/mdl_quote_amounts');

        $quote_id = $db_array['quote_id'] ?? $this->input->post('quote_id');

        if ($quote_id) {
            $global_discount['item'] = $this->mdl_quote_amounts->get_global_discount($quote_id);
            // Recalculate quote amounts
            $this->mdl_quote_amounts->calculate($quote_id, $global_discount);
        }
    }

    /**
     * @return array
     * @return void
     */
    public function validation_rules()
    {
        return [
            'quote_id' => [
                'field' => 'quote_id',
                'label' => trans('quote'),
                'rules' => 'required',
            ],
            'tax_rate_id' => [
                'field' => 'tax_rate_id',
                'label' => trans('tax_rate'),
                'rules' => 'required',
            ],
            'include_item_tax' => [
                'field' => 'include_item_tax',
                'label' => trans('tax_rate_placement'),
                'rules' => 'required',
            ],
        ];
    }
}
