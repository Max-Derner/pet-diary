[Welcome Page](../README.md)

## *__Cost breakdown__*
__DISCLAIMER__: This breakdown is only done to the best of my abilities, I cannot guarantee any running costs at all.  

* __DynamoDB__:
    * 25 Read Capacity Units for free
    * 25 Write Capacity Units for free
    * Point In Time Recovery: $0.23772 per GB-month (can comment out in [template.yaml](../template.yaml))
* __KMS Key__: 
    * $1 per key generated (can comment out in [template.yaml](../template.yaml))
    * Gets 20,000 requests free per month

