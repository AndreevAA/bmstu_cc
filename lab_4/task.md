
| G                                          | S                                              |
| ------------------------------------------ | ---------------------------------------------- |
| expression -> relation                     | res = rel.res                                  |
| expression1 -> relation logic expression2  | res = logic  rel1.res  expression2.res         |
| relation ->  smplStmt                      | res = smplStmt.res                             |
| relation -> smplStmt1  relOp smplStmt2     | res = relOp smplStmt1.res smplStmt2.res        |
| smplStmt -> slag                           | res = slag.res                                 |
| smplStmt -> unar slag                      | res = unar 0 slag.res                          |
| smplStmt1 -> unar slag binar_add smplStmt2 | res = binar_add unar 0 slag1.res smplStmt2.res |
| slag -> mnoz                               | res = mnoz.res                                 |
| slag -> mnoz mult_op slag                  | res = mult_op mnoz.res slag.res                |
| mnoz -> first ** perv                      | res = ** first.res mnoz.res                    |
| mnoz -> abs perv                           | res = abs perv.res                             |
| mnoz -> not perv                           | res = not perv.res                             |

