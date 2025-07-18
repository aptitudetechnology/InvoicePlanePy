
<div class="table-responsive">
    <table id="item_table" class="items table table-condensed table-bordered no-margin">

        <thead style="display:none">
        <tr>
            <th></th>
            <th><?php _trans('item'); ?></th>
<!--
            <th><?php _trans('description'); ?></th>
-->
            <th class="amount"><?php _trans('quantity'); ?></th>
            <th class="amount"><?php _trans('price'); ?></th>
            <?php echo $legacy_calculation ? '' : '<th class="amount">' . trans('item_discount') . '</th>' ?>
            <th class="amount"><?php _trans('tax_rate'); ?></th>
            <?php echo $legacy_calculation ? '<th class="amount">' . trans('item_discount') . '</th>' : '' ?>
<!--
            <th class="amount"><?php _trans('subtotal'); ?></th>
            <th class="amount"><?php _trans('tax'); ?></th>
-->
            <th class="amount"><?php _trans('total'); ?></th>
            <th></th>
        </tr>
        </thead>

        <tbody id="new_row" style="display:none">
        <tr>
            <td rowspan="2" class="td-icon"><i class="fa fa-arrows cursor-move"></i></td>
            <td class="td-text">
                <input type="hidden" name="quote_id" value="<?php echo $quote_id; ?>">
                <input type="hidden" name="item_id" value="">
                <input type="hidden" name="item_product_id" value="">

                <div class="input-group">
                    <span class="input-group-addon"><?php _trans('item'); ?></span>
                    <input type="text" name="item_name" class="form-control" value="">
                </div>
            </td>
            <td class="td-amount td-quantity">
                <div class="input-group">
                    <span class="input-group-addon"><?php _trans('quantity'); ?></span>
                    <input type="text" name="item_quantity" class="form-control amount" value="">
                </div>
            </td>
            <td class="td-amount">
                <div class="input-group">
                    <span class="input-group-addon"><?php _trans('price'); ?></span>
                    <input type="text" name="item_price" class="form-control amount" value="">
                    <div class="input-group-addon"><?php echo get_setting('currency_symbol'); ?></div>
                </div>
            </td>
<?php
if ( ! $legacy_calculation) {
    $this->layout->load_view('layout/partial/itemlist_table_item_discount_input');
}
?>
            <td class="td-amount">
                <div class="input-group">
                    <span class="input-group-addon"><?php _trans('tax_rate'); ?></span>
                    <select name="item_tax_rate_id" class="form-control">
                        <option value="0"><?php _trans('none'); ?></option>
                        <?php foreach ($tax_rates as $tax_rate) { ?>
                            <option value="<?php echo $tax_rate->tax_rate_id; ?>">
                                <?php echo format_amount($tax_rate->tax_rate_percent) . '% - ' . $tax_rate->tax_rate_name; ?>
                            </option>
                        <?php } ?>
                    </select>
                </div>
            </td>
<?php
if ($legacy_calculation) {
    $this->layout->load_view('layout/partial/itemlist_table_item_discount_input');
}
?>
            <td class="td-icon text-right td-vert-middle">
                <button type="button" class="btn_delete_item btn btn-link btn-sm" title="<?php _trans('delete'); ?>">
                    <i class="fa fa-trash-o text-danger"></i>
                </button>
            </td>
        </tr>
        <tr>
            <td class="td-textarea">
                <div class="input-group">
                    <span class="input-group-addon"><?php _trans('description'); ?></span>
                    <textarea name="item_description" class="form-control"></textarea>
                </div>
            </td>
            <td class="td-amount">
                <div class="input-group">
                    <span class="input-group-addon"><?php _trans('product_unit'); ?></span>
                    <select name="item_product_unit_id"
                            class="form-control">
                        <option value="0"><?php _trans('none'); ?></option>
                        <?php foreach ($units as $unit) { ?>
                            <option value="<?php echo $unit->unit_id; ?>">
                                <?php echo htmlsc($unit->unit_name) . '/' . htmlsc($unit->unit_name_plrl); ?>
                            </option>
                        <?php } ?>
                    </select>
                </div>
            </td>
            <td class="td-amount td-vert-middle">
                <span><?php _trans('subtotal'); ?></span><br/>
                <span name="subtotal" class="amount"></span>
            </td>
<?php
if ( ! $legacy_calculation) {
    $this->layout->load_view('layout/partial/itemlist_table_item_discount_show');
}
?>
            <td class="td-amount td-vert-middle">
                <span><?php _trans('tax'); ?></span><br/>
                <span name="item_tax_total" class="amount"></span>
            </td>
<?php
if ($legacy_calculation) {
    $this->layout->load_view('layout/partial/itemlist_table_item_discount_show');
}
?>
            <td class="td-amount td-vert-middle">
                <span><?php _trans('total'); ?></span><br/>
                <span name="item_total" class="amount"></span>
            </td>
        </tr>
        </tbody>

<?php
foreach ($items as $item) {
?>
        <tbody class="item">
            <tr>
                <td rowspan="2" class="td-icon"><i class="fa fa-arrows cursor-move"></i></td>
                <td class="td-text">
                    <input type="hidden" name="quote_id" value="<?php echo $quote_id; ?>">
                    <input type="hidden" name="item_id" value="<?php echo $item->item_id; ?>">
                    <input type="hidden" name="item_product_id" value="<?php echo $item->item_product_id; ?>">

                    <div class="input-group">
                        <span class="input-group-addon"><?php _trans('item'); ?></span>
                        <input type="text" name="item_name" class="form-control"
                               value="<?php _htmlsc($item->item_name); ?>">
                    </div>
                </td>
                <td class="td-amount td-quantity">
                    <div class="input-group">
                        <span class="input-group-addon"><?php _trans('quantity'); ?></span>
                        <input type="text" name="item_quantity" class="form-control amount"
                               value="<?php echo format_quantity($item->item_quantity); ?>">
                    </div>
                </td>
                <td class="td-amount">
                    <div class="input-group">
                        <span class="input-group-addon"><?php _trans('price'); ?></span>
                        <input type="text" name="item_price" class="form-control amount"
                               value="<?php echo format_amount($item->item_price); ?>">
                        <div class="input-group-addon"><?php echo get_setting('currency_symbol'); ?></div>
                    </div>
                </td>
<?php
    if ( ! $legacy_calculation) {
        $this->layout->load_view('layout/partial/itemlist_table_item_discount_input', ['item' => $item]);
    }
?>
                <td class="td-amount">
                    <div class="input-group">
                        <span class="input-group-addon"><?php _trans('tax_rate'); ?></span>
                        <select name="item_tax_rate_id" class="form-control">
                            <option value="0"><?php _trans('none'); ?></option>
<?php
    foreach ($tax_rates as $tax_rate) {
        $is_selected = ($item->item_tax_rate_id == $tax_rate->tax_rate_id) ? ' selected="selected"' : '';
?>
                            <option value="<?php echo $tax_rate->tax_rate_id; ?>"<?php echo $is_selected; ?>>
                                <?php echo format_amount($tax_rate->tax_rate_percent) . '% - ' . htmlsc($tax_rate->tax_rate_name); ?>
                            </option>
<?php
    }
?>
                        </select>
                    </div>
                </td>
<?php
    if ($legacy_calculation) {
        $this->layout->load_view('layout/partial/itemlist_table_item_discount_input', ['item' => $item]);
    }
?>
                <td class="td-icon text-right td-vert-middle">
                    <button type="button" class="btn_delete_item btn btn-link btn-sm" title="<?php _trans('delete'); ?>"
                            data-item-id="<?php echo $item->item_id; ?>">
                        <i class="fa fa-trash-o text-danger"></i>
                    </button>
                </td>
            </tr>
            <tr>
                <td class="td-textarea">
                    <div class="input-group">
                        <span class="input-group-addon"><?php _trans('description'); ?></span>
                        <textarea name="item_description" class="form-control"
                        ><?php echo htmlsc($item->item_description); ?></textarea>
                    </div>
                </td>
                <td class="td-amount">
                    <div class="input-group">
                        <span class="input-group-addon"><?php _trans('product_unit'); ?></span>
                        <select name="item_product_unit_id"
                                class="form-control">
                            <option value="0"><?php _trans('none'); ?></option>
<?php
    foreach ($units as $unit) {
?>
                            <option value="<?php echo $unit->unit_id; ?>"
                                <?php check_select($item->item_product_unit_id, $unit->unit_id); ?>>
                                <?php echo htmlsc($unit->unit_name) . '/' . htmlsc($unit->unit_name_plrl); ?>
                            </option>
<?php
    }
?>
                        </select>
                    </div>
                </td>
                <td class="td-amount td-vert-middle">
                    <span><?php _trans('subtotal'); ?></span><br/>
                    <span name="subtotal" class="amount">
                        <?php echo format_currency($item->item_subtotal); ?>
                    </span>
                </td>
<?php
    if ( ! $legacy_calculation) {
        $this->layout->load_view('layout/partial/itemlist_table_item_discount_show', ['item' => $item]);
    }
?>
                <td class="td-amount td-vert-middle">
                    <span><?php _trans('tax'); ?></span><br/>
                    <span name="item_tax_total" class="amount">
                        <?php echo format_currency($item->item_tax_total); ?>
                    </span>
                </td>
<?php
    if ($legacy_calculation) {
        $this->layout->load_view('layout/partial/itemlist_table_item_discount_show', ['item' => $item]);
    }
?>
                <td class="td-amount td-vert-middle">
                    <span><?php _trans('total'); ?></span><br/>
                    <span name="item_total" class="amount">
                        <?php echo format_currency($item->item_total); ?>
                    </span>
                </td>
            </tr>
        </tbody>
<?php
} // End foreach items
?>

    </table>
</div>

<br>

<div class="row">
    <div class="col-xs-12 col-md-4">
        <div class="btn-group">
            <a href="javascript:void(0);" class="btn_add_row btn btn-sm btn-default">
                <i class="fa fa-plus"></i>
                <?php _trans('add_new_row'); ?>
            </a>
            <a href="javascript:void(0);" class="btn_add_product btn btn-sm btn-default">
                <i class="fa fa-database"></i>
                <?php _trans('add_product'); ?>
            </a>
        </div>
    </div>

    <div class="col-xs-12 visible-xs visible-sm"><br></div>

    <div class="col-xs-12 col-md-6 col-md-offset-2 col-lg-4 col-lg-offset-4">
        <table class="table table-bordered text-right">
<?php
if ( ! $legacy_calculation) {
    $this->layout->load_view('quotes/partial_itemlist_table_quote_discount');
}
?>
            <tr>
                <td style="width: 40%;"><?php _trans('subtotal'); ?></td>
                <td style="width: 60%;" class="amount"><?php echo format_currency($quote->quote_item_subtotal); ?></td>
            </tr>
            <tr>
                <td><?php _trans('item_tax'); ?></td>
                <td class="amount"><?php echo format_currency($quote->quote_item_tax_total); ?></td>
            </tr>
<?php
if ($legacy_calculation) {
?>
            <tr>
                <td><?php _trans('quote_tax'); ?></td>
                <td>
<?php
    if ($quote_tax_rates) {
        foreach ($quote_tax_rates as $quote_tax_rate) {
?>
                    <form method="POST" class="form-inline"
                          action="<?php echo site_url('quotes/delete_quote_tax/' . $quote->quote_id . '/' . $quote_tax_rate->quote_tax_rate_id) ?>">
                        <?php _csrf_field(); ?>
                        <button type="submit" class="btn btn-xs btn-link" onclick="var Y=confirm('<?php _trans('delete_tax_warning'); ?>');if(Y)show_loader();return Y;">
                            <i class="fa fa-trash-o"></i>
                        </button>
                        <span class="text-muted">
                            <?php echo htmlsc($quote_tax_rate->quote_tax_rate_name) . ' ' . format_amount($quote_tax_rate->quote_tax_rate_percent) . '%' ?>
                        </span>
                        <span class="amount">
                            <?php echo format_currency($quote_tax_rate->quote_tax_rate_amount); ?>
                        </span>
                    </form>
<?php
        }
    } else {
        echo format_currency('0');
    }
?>
                </td>
            </tr>
<?php
    $this->layout->load_view('quotes/partial_itemlist_table_quote_discount');
}
?>
            <tr>
                <td><b><?php _trans('total'); ?></b></td>
                <td class="amount"><b><?php echo format_currency($quote->quote_total); ?></b></td>
            </tr>
        </table>
    </div>

</div>
