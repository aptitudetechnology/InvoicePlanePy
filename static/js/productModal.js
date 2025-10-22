// static/js/productModal.js - MINIMAL TEST VERSION
console.log('=== PRODUCT MODAL JS LOADED ===');

class ProductModal {
  constructor() {
    console.log('ProductModal constructor');
    this.modal = null;
  }

  showModal() {
    console.log('showModal called - modal would open here');
    alert('Product modal test - working!');
  }

  static getInstance() {
    console.log('getInstance called');
    if (!window.productModalInstance) {
      window.productModalInstance = new ProductModal();
      console.log('Created new instance');
    } else {
      console.log('Returning existing instance');
    }
    return window.productModalInstance;
  }
}

console.log('ProductModal class created:', typeof ProductModal);

// Auto-init
if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', () => ProductModal.getInstance());
} else {
  ProductModal.getInstance();
}

console.log('=== PRODUCT MODAL JS END ===');
