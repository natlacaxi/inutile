main :: IO ()
main = do
  l <- getLine
  let (v, rest) = break (== '\t') l
  putStrLn (v ++ "\t" ++ drop 1 rest ++ ">Haskell")
