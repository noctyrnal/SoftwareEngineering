document.addEventListener('DOMContentLoaded', function () {
    //  Flash Notifications
    const flashEl = document.getElementById('flash-messages');
    if (flashEl) {
        try {
            const flashMessages = JSON.parse(flashEl.textContent);
            flashMessages.forEach(msg => alert(msg));
        } catch (err) {
            console.error('Error parsing flash messages:', err);
        }
    }

    // 1️ Grab  menu data and key elements
    const menuItems    = JSON.parse(document.getElementById('menu-items').textContent);
    const formsetDiv   = document.getElementById('formset');
    const addButton    = document.getElementById('add-form');
    const totalForms   = document.getElementById('id_form-TOTAL_FORMS');
    const totalDisplay = document.getElementById('total-price');

    if (!formsetDiv || !addButton || !totalForms) {
        console.error("Missing #formset, #add-form or #id_form-TOTAL_FORMS");
        return;
    }

    // 2️ Capture the ORIGINAL category <option> HTML once
    const originalCategoryOptions =
        document.querySelector('.category-select').innerHTML;

    // Helpers -----------------------------------------------------------------

    function updateFormAttributes(form, index) {
        form.querySelectorAll('input, select, label').forEach(el => {
            if (el.name)     el.name     = el.name.replace(/form-\d+|__prefix__/, `form-${index}`);
            if (el.id)       el.id       = el.id.replace(/form-\d+|__prefix__/, `form-${index}`);
            if (el.htmlFor)  el.htmlFor  = el.htmlFor.replace(/form-\d+|__prefix__/, `form-${index}`);
        });
    }

    function updateTotal() {
        let total = 0;
        formsetDiv.querySelectorAll('.item-form').forEach(row => {
            const qty   = parseInt(row.querySelector('input[name$="-quantity"]').value || 0);
            const price = parseFloat(row.querySelector('.item-price').textContent || "0");
            total += qty * price;
        });
        totalDisplay.textContent = total.toFixed(2);
    }

    function setUpRowEvents(row) {
        const categorySelect = row.querySelector('.category-select');
        const itemSelect     = row.querySelector('select[name$="-menu_item"]');
        const priceSpan      = row.querySelector('.item-price');
        const qtyInput       = row.querySelector('input[name$="-quantity"]');

        function updateItemOptions() {
            const cat = categorySelect.value;
            itemSelect.innerHTML = '<option value="">---------</option>';
            menuItems
                .filter(i => i.category === cat)
                .forEach(i => {
                    const o = document.createElement('option');
                    o.value = i.id;
                    o.textContent = i.name;
                    itemSelect.appendChild(o);
                });
            updatePrice();
        }

        function updatePrice() {
            const sel = itemSelect.value;
            const m   = menuItems.find(i => i.id == sel);
            priceSpan.textContent = m ? parseFloat(m.price).toFixed(2) : "0.00";
            updateTotal();
        }

        categorySelect.addEventListener('change', updateItemOptions);
        itemSelect.addEventListener('change',   updatePrice);
        qtyInput.addEventListener('input',      updateTotal);

        row.querySelector('.remove-form').addEventListener('click', () => {
            const rows = formsetDiv.querySelectorAll('.item-form');
            if (rows.length <= 1) return alert("At least one item is required.");
            row.remove();
            formsetDiv.querySelectorAll('.item-form').forEach((r, i) => updateFormAttributes(r, i));
            totalForms.value = formsetDiv.querySelectorAll('.item-form').length;
            updateTotal();
        });

        updateItemOptions();
    }

    // Initialize existing rows ---------
    formsetDiv.querySelectorAll('.item-form').forEach(setUpRowEvents);
    updateTotal();

    // Add-Item button -----------
    addButton.addEventListener('click', () => {
        const count   = parseInt(totalForms.value);
        const first   = document.querySelector('.item-form');
        const newForm = first.cloneNode(true);

        // Re-inject the original category options
        const catSel = newForm.querySelector('.category-select');
        catSel.innerHTML = originalCategoryOptions;

        // Clear the menu_item dropdown
        newForm.querySelector('select[name$="-menu_item"]').innerHTML = '<option value="">---------</option>';

        // Reset quantity & price
        newForm.querySelector('input[name$="-quantity"]').value    = 1;
        newForm.querySelector('.item-price').textContent           = '0.00';

        // Fix up form-* indices
        updateFormAttributes(newForm, count);

        // Append & update management form
        formsetDiv.appendChild(newForm);
        totalForms.value = count + 1;

        // Bind events & trigger initial population
        setUpRowEvents(newForm);
        newForm.querySelector('.category-select').dispatchEvent(new Event('change'));
    });
});
