const cds = require('@sap/cds');
const cors = require('cors');
const path = require('path');
const express = require('express');

cds.on('bootstrap', (app) => {
    // Enable CORS for all origins and headers
    app.use(cors());

    // Serve frontend webapp directly from CAP
    const webappPath = path.resolve(__dirname, '../sap-ui5-frontend/webapp');
    app.use('/webapp', express.static(webappPath));
    
    // Redirect root to webapp if HTML is requested
    app.get('/', (req, res, next) => {
        if (req.accepts('html')) {
            return res.redirect('/webapp/index.html');
        }
        next();
    });
});

module.exports = cds.server;
