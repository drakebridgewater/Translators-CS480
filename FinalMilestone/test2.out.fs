6 7 + 
 2 11 * 
 5 8 % 
 4 9 - 
 10 2 / 
 variable x x 10 
 20 x @ - . 
 : ifloop49 x @ 1 > if s" yes1" TYPE else then ; 
ifloop49
 : ifloop61 x @ 2 < if s" yes2" s"  true" s+ TYPE else s" no2" s"  true" s+ TYPE else then ; 
ifloop61
 : ifloop85 x @ 3 < if s" yes3" s"  true" s+ TYPE else s" no3" s"  true" s+ TYPE else then ; 
ifloop85
 : ifloop109 x @ 4 < if s" yes4" TYPE else then ; 
ifloop109
 x 15 
 : whilestmts126 BEGIN x @ 5 > while s" hello5" TYPE  x @ 1 - x ! x @ TYPE  TYPE  x @ 6 > TYPE  s" yes6" REPEAT ; 
whilestmts126
 variable n variable a variable b variable area variable width variable x n 100 
 a 0 
 b 1 
 area 0 
 x a 
 width b @ - n 
 
 : whilestmts226 BEGIN x @ b < while area @ + area ! area @ TYPE  x @ 2 ^ REPEAT ; 
whilestmts226
 
 
 
 x x @ + 
 
 
 
 cr cr bye 