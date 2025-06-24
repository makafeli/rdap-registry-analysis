#!/bin/bash

# RDAP Registrar Enrichment Script
# This script fetches contact information for Registry Gateway registrars from ICANN API

echo "=== RDAP Registrar Enrichment Script ==="
echo "Fetching contact information from ICANN API..."
echo ""

# Create output directory
mkdir -p ../data

# Output file
OUTPUT_FILE="../data/enriched_registrars.csv"

# Write CSV header
echo "iana_id,name,website,email,phone,abuse_email,whois_server,status,city,country,rdap_url,domains" > $OUTPUT_FILE

# Registry Gateway registrar IANA IDs (top 20 by domain count)
IANA_IDS=(
    303   # PDR Ltd.
    955   # Launchpad.com Inc.
    1636  # Hostinger, UAB
    1495  # BigRock Solutions Ltd.
    1091  # IHS Telekom, Inc.
    1005  # NetEarth One Inc.
    609   # Sav.com, LLC
    1586  # MAT BAO CORPORATION
    3806  # Beget LLC
    1600  # Tecnocrática Centro de Datos
    1432  # Alpine Domains Inc.
    1534  # Aerotek Bilisim
    819   # Reg2C.com Inc.
    1483  # Neubox Internet
    1710  # Nhan Hoa Software
    1112  # Internet Invest
    1913  # DOTSERVE INC.
    1895  # Namespro Solutions
    1082  # Register4Less
    1660  # Domainshype.com
)

# Domain counts for each registrar
DOMAIN_COUNTS=(
    4845099  # PDR Ltd.
    729662   # Launchpad.com Inc.
    590290   # Hostinger, UAB
    276454   # BigRock Solutions Ltd.
    160821   # IHS Telekom, Inc.
    142479   # NetEarth One Inc.
    135595   # Sav.com, LLC
    134504   # MAT BAO CORPORATION
    103122   # Beget LLC
    101516   # Tecnocrática Centro de Datos
    81068    # Alpine Domains Inc.
    80389    # Aerotek Bilisim
    75272    # Reg2C.com Inc.
    62661    # Neubox Internet
    57102    # Nhan Hoa Software
    47650    # Internet Invest
    41645    # DOTSERVE INC.
    38321    # Namespro Solutions
    33943    # Register4Less
    33214    # Domainshype.com
)

# Counter for progress
COUNTER=0
TOTAL=${#IANA_IDS[@]}

# Function to fetch registrar data
fetch_registrar_data() {
    local iana_id=$1
    local domain_count=$2
    
    echo "[$((COUNTER + 1))/$TOTAL] Fetching data for IANA ID: $iana_id"
    
    # Fetch from ICANN API
    RESPONSE=$(curl -s "https://lookup.icann.org/api/registrar/$iana_id")
    
    # Check if we got a response
    if [ -z "$RESPONSE" ]; then
        echo "  - No response received for IANA ID $iana_id"
        return
    fi
    
    # Parse JSON response using jq
    if command -v jq &> /dev/null; then
        NAME=$(echo $RESPONSE | jq -r '.name // "N/A"' | sed 's/,/;/g')
        WEBSITE=$(echo $RESPONSE | jq -r '.url // "N/A"')
        EMAIL=$(echo $RESPONSE | jq -r '.email // "N/A"')
        PHONE=$(echo $RESPONSE | jq -r '.phone // "N/A"')
        ABUSE_EMAIL=$(echo $RESPONSE | jq -r '.abuseContact.email // "N/A"')
        WHOIS_SERVER=$(echo $RESPONSE | jq -r '.whoisServer // "N/A"')
        STATUS=$(echo $RESPONSE | jq -r '.status // "N/A"')
        CITY=$(echo $RESPONSE | jq -r '.address.city // "N/A"' | sed 's/,/;/g')
        COUNTRY=$(echo $RESPONSE | jq -r '.address.country // "N/A"')
        
        # Write to CSV
        echo "$iana_id,\"$NAME\",\"$WEBSITE\",\"$EMAIL\",\"$PHONE\",\"$ABUSE_EMAIL\",\"$WHOIS_SERVER\",\"$STATUS\",\"$CITY\",\"$COUNTRY\",\"rdapserver.net\",$domain_count" >> $OUTPUT_FILE
        
        echo "  - Successfully fetched: $NAME"
    else
        echo "  - Error: jq is not installed. Install it with: brew install jq"
        echo "$iana_id,\"Error: jq not installed\",\"\",\"\",\"\",\"\",\"\",\"\",\"\",\"\",\"rdapserver.net\",$domain_count" >> $OUTPUT_FILE
    fi
    
    # Rate limiting (1 request per second)
    sleep 1
}

# Main loop
for i in "${!IANA_IDS[@]}"; do
    fetch_registrar_data ${IANA_IDS[$i]} ${DOMAIN_COUNTS[$i]}
    ((COUNTER++))
done

echo ""
echo "=== Enrichment Complete ==="
echo "Results saved to: $OUTPUT_FILE"
echo "Total registrars processed: $COUNTER"

# Display summary
echo ""
echo "Sample results:"
head -5 $OUTPUT_FILE | column -t -s ','

echo ""
echo "To view all results, open: $OUTPUT_FILE"
