# AWSPricer - A Pricing API for AWS
#### Currently Supports EC2

---
## Major Revamp!!!

**Description:**
This is a pricing API for AWS. This currently supports EC2. I have created 
filters for products that can be built on top of each other to get backs lists
that can then be priced and returned.


**Example:**

```
products = pricer.filterproducts(vcpu='4', memory='16 GiB').filterprice(PurchaseOption='No Upfront').getprice()
    print (products)
```

The above exampe uses filterproducts, filterprice, and getprice

**.filterproducts(key=value):**
use this method in order to filter products by attributes.

**AWS Attributes and Example values:**

        "servicecode" : "AmazonEC2",     
        "location" : "US West (N. California)",
        "locationType" : "AWS Region",
        "instanceType" : "m4.xlarge",
        "currentGeneration" : "Yes",
        "instanceFamily" : "General purpose",
        "vcpu" : "4",
        "physicalProcessor" : "Intel Xeon E5-2676 v3 (Haswell)",
        "clockSpeed" : "2.4  GHz",
        "memory" : "16 GiB",
        "storage" : "EBS only",
        "networkPerformance" : "High",
        "processorArchitecture" : "64-bit",
        "tenancy" : "Host",
        "operatingSystem" : "Windows",
        "licenseModel" : "License Included",
        "usagetype" : "USW1-HostBoxUsage:m4.xlarge",
        "operation" : "RunInstances:0202",
        "dedicatedEbsThroughput" : "750 Mbps",
        "enhancedNetworkingSupported" : "Yes",
        "preInstalledSw" : "SQL Web",
        "processorFeatures" : "Intel AVX; Intel AVX2; Intel Turbo"
        
        
**.filterprice(key=value)**
use this method in order to filter price by terms.

**AWS Terms and example values**

            "LeaseContractLength" : "1yr",
            "OfferingClass" : "standard",
            "PurchaseOption" : "Partial Upfront"
      
**.getprice()**

this method is used to provide final pricing after filtering

**.getproducts()**

This metod is used to get products after filtering of products

*** Cannot use after getprice() or filteredpricing() ***
