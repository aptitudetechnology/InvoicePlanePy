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
class Tasks extends Admin_Controller
{
    /**
     * Tasks constructor.
     */
    public function __construct()
    {
        parent::__construct();

        $this->load->model('mdl_tasks');
    }

    /**
     * @param int $page
     */
    public function index($page = 0)
    {
        $this->mdl_tasks->paginate(site_url('tasks/index'), $page);
        $tasks = $this->mdl_tasks->result();

        $this->layout->set(
            [
                'filter_display'     => true,
                'filter_placeholder' => trans('filter_tasks'),
                'filter_method'      => 'filter_tasks',
                'tasks'              => $tasks,
                'task_statuses'      => $this->mdl_tasks->statuses(),
            ]
        );
        $this->layout->buffer('content', 'tasks/index');
        $this->layout->render();
    }

    public function form($id = null)
    {
        if ($this->input->post('btn_cancel')) {
            redirect('tasks');
        }

        $this->filter_input();  // <<<--- filters _POST array for nastiness

        if ($this->mdl_tasks->run_validation()) {
            $this->mdl_tasks->save($id);
            redirect('tasks');
        }

        if ( ! $this->input->post('btn_submit')) {
            $prep_form = $this->mdl_tasks->prep_form($id);
            if ($id && ! $prep_form) {
                show_404();
            }
        }

        $this->load->model('projects/mdl_projects');
        $this->load->model('tax_rates/mdl_tax_rates');

        $this->layout->set(
            [
                'projects'      => $this->mdl_projects->get()->result(),
                'task_statuses' => $this->mdl_tasks->statuses(),
                'tax_rates'     => $this->mdl_tax_rates->get()->result(),
            ]
        );
        $this->layout->buffer('content', 'tasks/form');
        $this->layout->render();
    }

    /**
     * @param $id
     */
    public function delete($id)
    {
        $this->mdl_tasks->delete($id);
        redirect('tasks');
    }
}
