import Prelude hiding (lookup)

data BinaryTree k v = Nil | Cons (k, v) (BinaryTree k v) (BinaryTree k v) deriving (Show, Eq)

insert k v Nil = Cons (k, v) Nil Nil
insert k v (Cons node tree1 tree2) | k == fst node = Cons (k, v) tree1 tree2
							       | k > fst node  = Cons node (insert k v tree1) tree2
							       | k < fst node  = Cons node tree1 (insert k v tree2)


lookup k Nil = Nothing
lookup k (Cons node tree1 tree2) | k == fst node = Just (snd node)
                                 | k > fst node  = lookup k tree1
                                 | k < fst node  = lookup k tree2
	
				
delete k (Cons node tree1 tree2) | k == fst node = merge tree1 tree2
                                 | k > fst node  = Cons node (delete k tree1) tree2
                                 | k < fst node  = Cons node tree1 (delete k tree2)
      where merge tree Nil = tree
            merge (Cons node tree11 tree12) tree2 = Cons node (merge tree11 tree12) tree2




