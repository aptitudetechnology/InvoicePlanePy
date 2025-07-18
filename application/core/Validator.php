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
class Validator extends MY_Model
{
    /**
     * @return bool
     */
    public function validate_text()
    {
        return true;
    }

    /**
     * @param $value
     *
     * @return bool|null
     */
    public function validate_date($value)
    {
        if ($value == '') {
            return;
        }

        if ( ! is_date($value)) {
            $this->form_validation->set_message('validate_date', trans('invalid_date'));

            return false;
        }

        return true;
    }

    /**
     * @param $value
     *
     * @return bool|null
     */
    public function validate_boolean($value)
    {
        if ($value == '0' || $value == '1') {
            return true;
        }

        if ($value == '') {
            return;
        }

        return false;
    }

    /**
     * @param string $value
     * @param int    $key
     *
     * @return bool|null
     */
    public function validate_singlechoice($value, $key)
    {
        if ($value == '') {
            return;
        }

        $this->load->model('custom_values/mdl_custom_values', 'custom_value');

        return $this->custom_value->column_has_value($key, $value);
    }

    /**
     * @param array $values
     * @param int   $id
     *
     * @return bool|null
     */
    public function validate_multiplechoice($values, $id)
    {
        // Fix unresetable (Origin only == '')
        if ($values == '' || $values[0] == '') { // work with str, array & null: See https://www.php.net/manual/function.is-null.php#87355
            return;
        }

        $this->load->model('custom_values/mdl_custom_values', 'custom_value');
        $this->custom_value->where('custom_field_id', $id);
        $dbvals = $this->custom_value->where_in('custom_values_id', $values)->get();

        return $dbvals->num_rows() == count($values);
    }

    /**
     * @return array
     */
    public function validation_rules()
    {
        return [
            'custom_field_table' => [
                'field' => 'custom_field_table',
                'label' => trans('table'),
                'rules' => 'required',
            ],
            'custom_field_label' => [
                'field' => 'custom_field_label',
                'label' => trans('label'),
                'rules' => 'required|max_length[50]',
            ],
            'custom_field_type' => [
                'field' => 'custom_field_type',
                'label' => trans('type'),
                'rules' => 'required',
            ],
        ];
    }

    /**
     * @param $column
     */
    public function get_field_type($column)
    {
        $this->load->model('custom_values/mdl_custom_fields', 'cf');
        $el = $this->cf->get_by_column($column)->row();

        if ($el == null) {
            return;
        }

        return $el->custom_field_type;
    }

    /**
     * @param $array
     *
     * @return bool|string
     */
    public function validate($array)
    {
        $this->load->model('custom_fields/mdl_custom_fields');
        $this->load->model('custom_values/mdl_custom_values');

        $db_array = $array;
        $errors   = [];

        if (empty($db_array)) {
            // Return true if no fields need to be validated
            return true;
        }

        foreach ($db_array as $key => $value) {
            $model = $this->mdl_custom_fields->where('custom_field_id', $key)->get();

            if ($model->num_rows()) {
                $model = $model->row();
/*
                if (@$model->custom_field_required == '1') // Todo implement (Only here & Not in db! Oldies?)
                {
                    if ($value == '') {
                        $errors[] = [
                            'field'     => $model->custom_field_id,
                            'label'     => $model->custom_field_label,
                            'error_msg' => 'missing field required',
                        ];
                        continue;
                    }
                }
*/
                $result = $this->validate_type($model->custom_field_type, $value, $key);

                if ($result === false) {
                    $errors[] = [
                        'field'     => $model->custom_field_id,
                        'label'     => $model->custom_field_label,
                        'error_msg' => 'invalid input',
                    ];
                }
            }
        }

        if (count($errors) == 0) {
            $this->_formdata = $db_array;
            $this->fixinput();

            return true;
        }

        return $this->create_error_text($errors);
    }

    /**
     * @param $type
     * @param $value
     * @param $key
     *
     * @return mixed
     */
    public function validate_type($type, $value, $key)
    {
        $nicename        = $this->mdl_custom_fields->get_nicename($type);
        $validation_rule = 'validate_' . $nicename;

        return $this->{$validation_rule}($value, $key);
    }

    public function fixinput()
    {
        foreach ($this->_formdata as $key => $value) {
            $model = $this->mdl_custom_fields->where('custom_field_id', $key)->get();

            if ($model->num_rows()) {
                $model = $model->row();
                $ftype = $model->custom_field_type;

                switch ($ftype) {
                    case 'DATE':
                        $this->_formdata[$key] = $value == '' ? null : date_to_mysql($value);

                        break;

                    case 'MULTIPLE-CHOICE':
                        $value                 = is_array($value) && $value[0] == '' ? null : $value; // reset if none in list
                        $this->_formdata[$key] = is_array($value) ? implode(',', $value) : $value;
                        break;

                    case 'TEXT':
                    case 'SINGLE-CHOICE':
                        if ($value == '') {
                            $this->_formdata[$key] = null;
                        }

                        break;
                }
            }
        }
    }

    /**
     * @param $errors
     *
     * @return string
     */
    public function create_error_text($errors)
    {
        $string = [];

        foreach ($errors as $error) {
            $string[] = sprintf(lang('validator_fail'), $error['label'], $error['error_msg']);
        }

        return nl2br(implode("\n", $string));
    }
}
