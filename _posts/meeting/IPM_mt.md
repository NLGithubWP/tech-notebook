# 11-07

1. After payment, transfer on click.
2. Deploy backend to AWS.
2. Add attachment: done

# 11-15

1. [phx] Test pipeline.
2. [phx] User management: 
   1. Refine documents. Public => subscribe user (login and subscribed) => paid user (login and paied) => collaborator => owner & institute admin. Level 1~5.
   2. Auto convert to un-publish if collaborator edits IP contents. (is publish = true only if the user is owner or institute admin.)
3. [phx] Once one user is editing the IP,  others cannot edit it. (lock timestamp)
   1. Collaborator update with auto-save as a heart-beat message. / The login-in token has a 1-hour time-out.
4. [phx] Create NFT by saving a PDF
   1. Accepting data-URL string from the front end.
   2. attachment []string --> hash and add into the GetHash()
5. [naili] Transfer ownership of IP once the IP is bought.
   1. Notification to the owner that others buy his NFT.
   2. Two new APIs BuyNFT, GetPurchaseRequests.
   3. Notification store collection => MongoDB.
6. [naili] HTTPS SSL Certification.
7. [phx, NL ] Performance
   1. Images performance.
   2. Per-Page modification.
   3. Indexes for MongoDB.
   4. Cache Search./NFT cache with the lease.
8. [phx] Bug fix:
   1. Double quote error.
   2. length errors.

# 11-18

1. HTTPs redeployment. 

# 11-22

1. khjk
2. kjh
3. jh
4. kjh

















