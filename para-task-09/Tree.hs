import Prelude hiding (lookup)

data BinaryTree k v = Nil | Cons (k, v) (BinaryTree k v) (BinaryTree k v) deriving (Show, Eq)

insert k v Nil = Cons (k, v) Nil Nil
insert k v (Cons node@(k', v') tree1 tree2) | k == k' = Cons node tree1 tree2
                                            | k < k'  = Cons node (insert k v tree1) tree2
                                            | k > k'  = Cons node tree1 (insert k v tree2)


lookup k Nil = Nothing
lookup k (Cons (k', v) tree1 tree2) | k == k' = Just v
                                    | k < k'  = lookup k tree1
                                    | k > k'  = lookup k tree2


delete k (Cons node@(k', v) tree1 tree2) | k == k' = merge tree1 tree2
                                         | k < k'  = Cons node (delete k tree1) tree2
                                         | k > k'  = Cons node tree1 (delete k tree2)
      where merge Nil tree = tree
            merge (Cons node tree11 tree12) tree2 = Cons node tree11 (merge tree12 tree2)


