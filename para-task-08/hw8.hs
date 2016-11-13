head' a = a !! 0

tail' (x:xs) = xs

take' 0 a = []
take' n a =  head' a : (take' (n - 1) (tail a))     

drop' 0 a = a
drop' _ [] = []
drop' n a = drop' (n - 1) (tail' a)

filter' f [] = []
filter' f a = if f (head' a) then
			   (head' a) : filter' f (tail' a)
			  else
				filter' f (tail' a)

foldl' f z [] = z				
foldl' f z l = foldl' f (f z (head' l)) (tail' l) 

concat' a b = a ++ b

quicksort' [] = []
quicksort' a = concat' (concat' (quicksort' (filter' (< head' a) a))  (filter' (== head' a) a))  (quicksort' (filter' (> head' a) a))

