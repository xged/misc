import           Control.Monad
import           Text.Parsec hiding (token)
import           Text.Parsec.String

type Atom = String

data Token = Raw Atom | Bold Atom | Italic Atom deriving (Show)

atom :: Parser Atom
atom = many1 (noneOf "*")

raw :: Parser Token
raw = liftM Raw $ atom

bold :: Parser Token
bold = liftM Bold $ between (string "**") (string "**") atom

italic :: Parser Token
italic = liftM Italic $ between (string "*") (string "*") atom

token :: Parser [Token]
token = many1 $ try raw <|> try bold <|> italic

main = do
    print (parse raw "" "atom")
    print (parse bold "" "**atom**")
    print (parse italic "" "*atom*")
    print (parse token "" "*hello* **world**")
