head' (x:xs) = x

tail' [] = []
tail' (x:xs) = xs

take' 0 _ = []
take' n (x:xs) =  x : (take' (n - 1) xs)     

drop' 0 a = a
drop' _ [] = []
drop' n (x:xs) = drop' (n - 1) xs

filter' _ [] = []
filter' f (x:xs) | f x       = x : filter' f xs
                 | otherwise = filter' f xs

foldl' _ z [] = z				
foldl' f z (x:xs) = foldl' f (f z x) xs 
  

concat' [] a = a
concat' (x:xs) a = x : (concat' xs a) 

quicksort' [] = []
quicksort' a = concat' (concat' (quicksort' (filter' (< head' a) a))  
                                            (filter' (== head' a) a))  
                                (quicksort' (filter' (> head' a) a))

