const XLSX = require('xlsx');
const fs = require('fs');
const path = require('path');

// Load and analyze RDAP data
function analyzeRDAPData(filePath) {
    console.log('=== RDAP Registry Analysis ===\n');
    
    // Read the Excel file
    const workbook = XLSX.readFile(filePath);
    
    // Get data from both sheets
    const listSheet = workbook.Sheets['List'];
    const domainCountSheet = workbook.Sheets['Domain count'];
    
    // Convert to JSON
    const registrarData = XLSX.utils.sheet_to_json(listSheet);
    const domainCounts = XLSX.utils.sheet_to_json(domainCountSheet, { header: 1 });
    
    // Create domain count map
    const domainCountMap = {};
    domainCounts.forEach(row => {
        if (row[0] && row[1]) {
            domainCountMap[row[0]] = row[1];
        }
    });
    
    // Enhance registrar data with domain counts
    const enhancedData = registrarData.map(registrar => ({
        ...registrar,
        domainCount: domainCountMap[registrar['Iana id']] || 0
    }));
    
    // Analyze Registry Gateway (rdapserver.net)
    const registryGatewayUsers = enhancedData.filter(r => r.rdap_url === 'rdapserver.net');
    const rgWithDomains = registryGatewayUsers.filter(r => r.domainCount > 0);
    const totalRGDomains = registryGatewayUsers.reduce((sum, r) => sum + r.domainCount, 0);
    
    console.log('Registry Gateway (LogicBoxes) Analysis:');
    console.log(`- Total users: ${registryGatewayUsers.length}`);
    console.log(`- Users with domain data: ${rgWithDomains.length}`);
    console.log(`- Total domains managed: ${totalRGDomains.toLocaleString()}`);
    console.log(`- Average domains per registrar: ${Math.round(totalRGDomains / rgWithDomains.length).toLocaleString()}\n`);
    
    // Top Registry Gateway users
    const topRGUsers = registryGatewayUsers
        .sort((a, b) => b.domainCount - a.domainCount)
        .slice(0, 10);
    
    console.log('Top 10 Registry Gateway Users:');
    topRGUsers.forEach((user, idx) => {
        console.log(`${idx + 1}. ${user.Name} (IANA ID: ${user['Iana id']}): ${user.domainCount.toLocaleString()} domains`);
    });
    
    // Overall RDAP provider statistics
    const rdapProviderStats = {};
    enhancedData.forEach(registrar => {
        const url = registrar.rdap_url;
        if (!rdapProviderStats[url]) {
            rdapProviderStats[url] = {
                count: 0,
                domains: 0,
                registrars: []
            };
        }
        rdapProviderStats[url].count++;
        rdapProviderStats[url].domains += registrar.domainCount;
        rdapProviderStats[url].registrars.push(registrar.Name);
    });
    
    // Sort by registrar count
    const topProviders = Object.entries(rdapProviderStats)
        .sort((a, b) => b[1].count - a[1].count)
        .slice(0, 5);
    
    console.log('\n\nTop 5 RDAP Providers by Registrar Count:');
    topProviders.forEach(([url, stats]) => {
        const percentage = ((stats.count / registrarData.length) * 100).toFixed(1);
        console.log(`- ${url}: ${stats.count} registrars (${percentage}%), ${stats.domains.toLocaleString()} domains`);
    });
    
    // Save Registry Gateway data to JSON
    const outputData = {
        summary: {
            totalRegistrars: registrarData.length,
            uniqueRdapUrls: Object.keys(rdapProviderStats).length,
            registryGateway: {
                provider: 'LogicBoxes',
                url: 'rdapserver.net',
                totalUsers: registryGatewayUsers.length,
                totalDomains: totalRGDomains,
                averageDomainsPerRegistrar: Math.round(totalRGDomains / rgWithDomains.length)
            }
        },
        registryGatewayUsers: registryGatewayUsers.map(r => ({
            ianaId: r['Iana id'],
            name: r.Name,
            domains: r.domainCount,
            rdapUrl: r.rdap_url
        })),
        topProviders: topProviders.map(([url, stats]) => ({
            url,
            registrarCount: stats.count,
            domainCount: stats.domains,
            percentage: ((stats.count / registrarData.length) * 100).toFixed(1)
        }))
    };
    
    // Save to file
    const outputPath = path.join(__dirname, '..', 'data', 'analysis_results.json');
    fs.writeFileSync(outputPath, JSON.stringify(outputData, null, 2));
    console.log(`\n\nAnalysis results saved to: ${outputPath}`);
}

// Main execution
if (process.argv.length < 3) {
    console.log('Usage: node analyze_rdap.js <path-to-excel-file>');
    console.log('Example: node analyze_rdap.js "../Rdap lookups.xlsx"');
    process.exit(1);
}

const filePath = process.argv[2];

if (!fs.existsSync(filePath)) {
    console.error(`Error: File not found - ${filePath}`);
    process.exit(1);
}

analyzeRDAPData(filePath);
