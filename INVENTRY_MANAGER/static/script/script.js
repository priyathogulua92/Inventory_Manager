var br = document.createElement("br");
        function ADD_ITEMS() {
          var form = document.getElementById("items_div");

          var brandDiv = document.createElement("div");
          var brandTag = document.createElement("label");
          var brand = document.createElement("input");
          brand.setAttribute("type", "text");
          brand.setAttribute("name", "brand");
          brandTag.setAttribute("class", "form-label");
          brandTag.innerHTML = "Brand";
          brandDiv.appendChild(brandTag);
          brandDiv.appendChild(brand);

          var productDiv = document.createElement("div");
          var productTag = document.createElement("label");
          var product = document.createElement("input");
          product.setAttribute("type", "text");
          product.setAttribute("name", "product");
          productTag.setAttribute("class", "form-label");
          productTag.innerHTML = "Product";
          productDiv.appendChild(productTag);
          productDiv.appendChild(product);

          var modelDiv = document.createElement("div");
          var modelTag = document.createElement("label");
          var model = document.createElement("input");
          model.setAttribute("type", "text");
          model.setAttribute("name", "model");
          modelTag.setAttribute("class", "form-label");
          modelTag.innerHTML = "Model";
          modelDiv.appendChild(modelTag);
          modelDiv.appendChild(model);

          var priceDiv = document.createElement("div");
          var priceTag = document.createElement("label");
          var price = document.createElement("input");
          price.setAttribute("type", "number");
          price.setAttribute("name", "price");
          priceTag.setAttribute("class", "form-label");
          priceTag.innerHTML = "Price";
          priceDiv.appendChild(priceTag);
          priceDiv.appendChild(price);

          var quantityDiv = document.createElement("div");
          var quantityTag = document.createElement("label");
          var quantity = document.createElement("input");
          quantity.setAttribute("type", "number");
          quantity.setAttribute("name", "quantity");
          quantityTag.setAttribute("class", "form-label");
          quantityTag.innerHTML = "Quantity";
          quantityDiv.appendChild(quantityTag);
          quantityDiv.appendChild(quantity);

          form.appendChild(br.cloneNode());
          form.appendChild(brandDiv);
          form.appendChild(productDiv);
          form.appendChild(modelDiv);
          form.appendChild(priceDiv);
          form.appendChild(quantityDiv);
        }