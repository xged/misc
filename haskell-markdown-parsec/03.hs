import           Control.Monad
import           Text.Parsec
import           Text.Parsec.String

type Atom = String

data Token = Raw Atom
           | Bold Atom
           | Italic Atom
           | Link Atom Atom
           deriving (Show)

inside :: String -> String -> Parser Atom
inside s1 s2 = between (string s1) (string s2) atom

atom :: Parser Atom
atom = many1 (noneOf "*[]()")

raw    :: Parser Token
bold   :: Parser Token
italic :: Parser Token
link   :: Parser Token
raw    = liftM Raw atom
bold   = liftM Bold $ inside "**" "**"
italic = liftM Italic $ inside "*" "*"
link   = liftM2 Link (inside "[" "]") $ inside "(" ")"

parser :: Parser [Token]
parser = many1 $ try raw <|> try bold <|> try italic <|> link

main = do
    s <- readFile "./data/text.md"
    print $ parse parser "" s
