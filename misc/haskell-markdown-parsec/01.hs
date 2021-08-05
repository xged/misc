import           Control.Monad
import           Text.Parsec
import           Text.Parsec.String

type Atom = String

data Token = Bold Atom | Italic Atom deriving (Show)

atom :: Parser Atom
atom = many1 (noneOf "*")

bold :: Parser Token
bold = liftM Bold $ between (string "**") (string "**") atom

italic :: Parser Token
italic = liftM Italic $ between (string "*") (string "*") atom

main = print (parse bold "" "**atom**") >> print (parse italic "" "*atom*")
