---
title: python memory bug reports
date: 2021-08-12
layout: post
active: journal
header-img: "img/postcover/post02.jpg"
categories: [practise]
---

# Python Memory

```python
# output.register_hook(lambda grad: self.backward_hook(grad, module))
output.register_hook(partial(self.backward_hook, module=module))
```

The 1st line will massup the reference, resulting in memory leak. 