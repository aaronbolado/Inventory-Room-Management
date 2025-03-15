document.addEventListener("DOMContentLoaded", function() {
    const editButtons = document.querySelectorAll(".edit-user-btn");
    const editModal = document.getElementById("editUserModal");

    const productIdInput = editModal.querySelector("#productId");
    const updateName = editModal.querySelector("#updateName");
    const updatePrice = editModal.querySelector("#updatePrice");
    const updateStock = editModal.querySelector("#updateStock");
    const updateROP = editModal.querySelector("#updateROP");
    const updateROQ = editModal.querySelector("#updateROQ");

    const deleteProductBtn = editModal.querySelector("#delete-product-btn");

    // OPEN EDIT PRODUCT MODAL
    editButtons.forEach(button => {
        button.addEventListener("click", function() {
            const productId = this.closest("tr").dataset.id;

            fetch(`/product/${productId}`)
                .then(response => {
                    if (!response.ok) {
                        throw new Error('Network response was not ok');
                    }
                    return response.json();
                })
                .then(product => {
                    // Populate modal with product data
                    productIdInput.value = product.id;
                    updateName.value = product.name;
                    updatePrice.value = product.unit_price;
                    updateStock.value = product.qty_in_stock;
                    updateROP.value = product.reorder_point;
                    updateROQ.value = product.reorder_quantity;
                    
                    optSetupCost.value = product.setup_cost;
                    optOrderingCost.value = product.ordering_cost;
                    optHoldingCost.value = product.holding_cost;
                    optLeadTime.value = product.lead_time;

                    $(editModal).modal("show");
                })
                .catch(error => {
                    console.error('Error fetching product:', error);
                });
        });
    });
    
    // SHOW EDIT MODAL
    $(document).on('click', '.edit-user-btn', function() {
        var row = $(this).closest('tr');
        var productId = row.data('id');

        fetch(`/product/${productId}`)
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(product => {
            // Populate modal with product data
            productIdInput.value = product.id;
            updateName.value = product.name;
            updatePrice.value = product.unit_price;
            updateStock.value = product.qty_in_stock;
            updateROP.value = product.reorder_point;
            updateROQ.value = product.reorder_quantity;
            
            optSetupCost.value = product.setup_cost;
            optOrderingCost.value = product.ordering_cost;
            optHoldingCost.value = product.holding_cost;
            optLeadTime.value = product.lead_time;

            $(editModal).modal("show");
        })
        .catch(error => {
            console.error('Error fetching product:', error);
        });
    });

    // DELETE PRODUCT
    deleteProductBtn.addEventListener("click", function() {
        const productId = productIdInput.value;

        fetch(`/delete/${productId}`, {
            method: "DELETE"
        })
        .then(response => {
            if (response.ok) {
                console.log("Product deleted successfully.");
                $(editModal).modal("hide");
                
            } else {
                console.error("Failed to delete product.");
            }
        })
        .then(data => {
            console.log("Response data:", data);
            window.location.href = "/dashboard";
        })
        .catch(error => {
            console.error("Error:", error);
        });
    });

    // OPTIMIZE PRODUCT WITH HILL CLIMB AND ROP FUNCTION
    const optimizeForm = document.getElementById("optimize-form");
    const optSetupCost = editModal.querySelector("#setup_cost"); 
    const optOrderingCost = editModal.querySelector("#ordering_cost"); 
    const optHoldingCost = editModal.querySelector("#holding_cost"); 
    const optLeadTime = editModal.querySelector("#lead_time");

    optimizeForm.addEventListener('submit', function(event) {
        event.preventDefault();

        const formData = new FormData(this);
        const jsonData = {};
        formData.forEach((value, key) => {
            jsonData[key] = value;
        });
    
        const updateROPValue = document.getElementById('updateROP').value; 
        const updateROQValue = document.getElementById('updateROQ').value;
        const optProdId = productIdInput.value;
    
        jsonData['updateROP'] = updateROPValue;
        jsonData['updateROQ'] = updateROQValue;
        jsonData['product_id'] = optProdId;

        fetch('/optimize', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(jsonData)
        })
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                console.error('Error:', data.error);
            } else {
                // Display results
                document.getElementById('results').style.display = 'block';
                document.getElementById('optimized-roq').textContent = `Optimized Reorder Quantity: ${data.optimized_quantity}`;
                document.getElementById('optimized-rop').textContent = `Optimized Reorder Point: ${data.optimized_rop}`;
                document.getElementById('total-cost').textContent = `Total Cost: ${data.optimized_cost.toFixed(2)}`;
                document.getElementById('iterations').textContent = `Iterations: ${data.iterations}`;
            }
        })
        .catch(error => {
            console.error('Error:', error);
        });
    });

    // UPDATE PRODUCT
    document.getElementById('save-changes-btn').addEventListener('click', function(event) {
        event.preventDefault();

        // Gather data from the Product Information form
        const productUpdateData = {};
        const updateForm = document.getElementById('update-form');
        if (updateForm) {
            updateForm.querySelectorAll('input').forEach(input => {
                if (input.value !== null && input.value !== undefined) { // Check if input is null or undefined
                    productUpdateData[input.name] = input.value;
                } else {
                    productUpdateData[input.name] = ''; 
                }
            });
        
        // Gather data from the Optimize form
        const optimizeFormData = {};
        const optimizeForm = document.getElementById('optimize-form');
        if (optimizeForm) {
            optimizeForm.querySelectorAll('input').forEach(input => {
                if (input.value !== null && input.value !== undefined) {
                    optimizeFormData[input.name] = input.value;
                } else {
                    optimizeFormData[input.name] = '';
                }
            });
        } else {
            console.error('Form not found: optimize-form');
        }
        
        // Combine data from both forms
        const combinedData = {
            ...productUpdateData,
            ...optimizeFormData
        };

        fetch('/update', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(combinedData) 
        })
        .then(response => response.json())
        .then(data => {
            console.log('Product updated:', data);
            window.location.href = '/dashboard';

            // Update values and return to dashboard
            updateName.value = product.name;
            updatePrice.value = product.unit_price;
            updateStock.value = product.qty_in_stock;
            updateROP.value = product.reorder_point;
            updateROQ.value = product.reorder_quantity;
            optSetupCost.value = product.setup_cost;
            optOrderingCost.value = product.ordering_cost;
            optHoldingCost.value = product.holding_cost;
            optLeadTime.value = product.lead_time;

        })
        .catch(error => {
            console.error('Error updating product:', error);
            window.location.href = '/dashboard'; // Return to dashboard
        });
        } else {
            console.error('Form not found: update-form');
        }
    });

    // ADD PRODUCT
    const productForm = document.getElementById("productForm");
    const submitButton = document.getElementById("add-product-btn");

    submitButton.addEventListener("click", function() {
        productForm.submit();
    });
});