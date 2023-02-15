# 11-07

1. After payment, transfer on click.
2. Deploy backend to AWS.
2. Add attachment: done

# 11-15

1. [phx] Test pipeline.
2. [phx] User management: 
   1. Refine documents. Public => subscribe user (login and subscribed) => paid user (login and paid) => collaborator => owner & institute admin. Level 1~5.
   2. Auto convert to un-publish if collaborator edits IP contents. (is publish = true only if the user is owner or institute admin.)
3. [phx] Once one user is editing the IP,  others cannot. (lock timestamp)
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
   2. Length errors.

# 11-18

1. HTTPS redeployment. 

# 11-22

1. Nothing

# 11-25

1. [Naili] Parse word document to IP content.

# 11-29

1. pass

# 12-02

1. Transfer, SuperAdmin, user 
2. SuperAdmin can sign 
3. Account user
   1. Collaborators edit the draft. 
   2. Collaborator, public, the restricted user. 

4. Collaborator
   1. non-concurrent. 
   2. Save the draft, and the IP manager receives a notification. 
5. Search, recommendations

6. SBIP usage.

# 12-06

1. Discuss notification with ZhongKai.
2. Collolator notify.
4. Super-admin has all user accounts.

# 12-09

1. add new tag collaborator.

# 2023-01-03

**dashboard**

1. Ip. Lab. The startup,  How many are created monthly?
2. One organization, How many Views, likes, and subscribers?

# 01-06

1. Word file heading/re-parse.
2. Word Image matching to each section
3. Add coordinator and password, 
4. trending:
   1. Update, viewed.

# 01-20

IPM => create Super Admin => 

1. Role

   1. super-admin:
      1.  **add manager &  add inventor.**
   2. manager
      1. Add collaborator ( **cross-institute.** )
      2. Create IP 
      3. `Publish IP`
      4. `Transfer IP`
      5. Modify IP
   3. Inventor: (机构用户)
      1. Add collaborator ( **cross-institute.** )
      2. Create IP
      3. Modify IP
      4. `Assign IP to manager`
   4. publish user:
      1. registered public user
         1. 付费功能
      2. un-registered public user. 

2. Relation: Collaborator

   1. nothing can do with role management. 

3. TASK

   1. 加一个 role inventor. (hx)

      1. Add collaborator must user exist and has instituted. （hx）

      2. super admin adds user 的时候，显示是manager or inventor. 

         1. get user and get inventor (hx)

         1. inventor

         1. inventor add collaborator.  (hx)

   1. 自动发送邮件 (not now)
   2. feature projects: 
      1. like 最多的.  (hx 测试)
   3. related：（NL  ： 对接ai API）
      1. 同机构 weight 高，同类型，内部随机
      2. 用similarity， 
      3. AI 的 API
   4. A public user cannot enter the page. (frontend)
   5. My post adds like,(frontend)

4. IP

   1. Public content => all users can visit
   2. Private to buyer

# 2-14

