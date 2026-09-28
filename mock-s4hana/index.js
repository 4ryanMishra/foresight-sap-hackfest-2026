const express = require('express');
const cors = require('cors');

const app = express();
app.use(cors());
app.use(express.json());

const PORT = process.env.PORT || 8080;

// ==========================================
// MOCK S/4HANA ADAPTER BEHAVIOR
// ==========================================
// All endpoints simulate the response structure 
// of a live S/4HANA OData API for FORESIGHT MVP
// ==========================================

// Mock Data Stores
const suppliers = {
    'SUP-001': { Supplier: 'SUP-001', SupplierName: 'Acme Corp', Country: 'TW', RiskClass: 'Low', Capacity: 10000 },
    'SUP-002': { Supplier: 'SUP-002', SupplierName: 'Global Parts', Country: 'DE', RiskClass: 'Low', Capacity: 5000 },
    'SUP-003': { Supplier: 'SUP-003', SupplierName: 'Risky Supplier', Country: 'VN', RiskClass: 'High', Capacity: 20000 }
};

const materials = {
    'MAT-100': { Material: 'MAT-100', MaterialName: 'Microcontroller X', BaseUnit: 'PC' },
    'MAT-200': { Material: 'MAT-200', MaterialName: 'Sensor Y', BaseUnit: 'PC' }
};

const inventory = [
    { Material: 'MAT-100', Plant: 'PLANT-A', UnrestrictedStock: 500 },
    { Material: 'MAT-100', Plant: 'PLANT-B', UnrestrictedStock: 1200 },
    { Material: 'MAT-200', Plant: 'PLANT-A', UnrestrictedStock: 5000 }
];

const purchaseOrders = [
    { PurchaseOrder: 'PO-9001', Supplier: 'SUP-001', Material: 'MAT-100', OrderQuantity: 5000, DeliveryDate: '2026-10-15' },
    { PurchaseOrder: 'PO-9002', Supplier: 'SUP-002', Material: 'MAT-200', OrderQuantity: 2000, DeliveryDate: '2026-10-10' }
];

const productionOrders = [
    { ProductionOrder: 'PRD-1001', Material: 'FIN-100', Plant: 'PLANT-A', TargetQuantity: 1000, StartDate: '2026-10-20' }
];

// --- Mock Endpoints ---

// Supplier Lookup (e.g. API_SUPPLIER)
app.get('/sap/opu/odata/sap/API_SUPPLIER/A_Supplier', (req, res) => {
    const id = req.query.$filter ? req.query.$filter.match(/'([^']+)'/)[1] : null;
    if (id && suppliers[id]) {
        return res.json({ d: { results: [suppliers[id]] } });
    }
    return res.json({ d: { results: Object.values(suppliers) } });
});

// Material Lookup (e.g. API_PRODUCT_SRV)
app.get('/sap/opu/odata/sap/API_PRODUCT_SRV/A_Product', (req, res) => {
    return res.json({ d: { results: Object.values(materials) } });
});

// Inventory Lookup (e.g. API_MATERIAL_STOCK_SRV)
app.get('/sap/opu/odata/sap/API_MATERIAL_STOCK_SRV/A_MaterialStock', (req, res) => {
    const materialId = req.query.$filter ? req.query.$filter.match(/Material eq '([^']+)'/)?.[1] : null;
    let results = inventory;
    if (materialId) {
        results = inventory.filter(i => i.Material === materialId);
    }
    return res.json({ d: { results } });
});

// PO Context Lookup
app.get('/sap/opu/odata/sap/API_PURCHASEORDER_PROCESS_SRV/A_PurchaseOrder', (req, res) => {
    return res.json({ d: { results: purchaseOrders } });
});

// Production Order Context Lookup
app.get('/sap/opu/odata/sap/API_PRODUCTION_ORDER_SRV/A_ProductionOrder', (req, res) => {
    return res.json({ d: { results: productionOrders } });
});

// Recovery Transaction Simulation (Create PO)
app.post('/sap/opu/odata/sap/API_PURCHASEORDER_PROCESS_SRV/A_PurchaseOrder', (req, res) => {
    const payload = req.body;
    console.log(`[MOCK S/4] Simulated PO Creation for Supplier: ${payload.Supplier}, Material: ${payload.Material}`);
    
    // Simulate successful transaction
    res.status(201).json({
        d: {
            PurchaseOrder: `PO-SIM-${Math.floor(Math.random() * 10000)}`,
            Supplier: payload.Supplier,
            Status: 'Created Locally'
        }
    });
});

app.listen(PORT, () => {
    console.log(`[MOCK S/4] Adapter running on http://localhost:${PORT}`);
    console.log(`[MOCK S/4] READY for verifiable local FORESIGHT testing.`);
});
