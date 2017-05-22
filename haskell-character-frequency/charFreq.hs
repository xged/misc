{-# LANGUAGE TemplateHaskell #-}

module LetterFreq where

import qualified Control.Arrow as CA
import qualified Data.ByteString.Char8 as DB
import qualified Data.Char as DC
import qualified Data.List as DL
import qualified Data.Map.Strict as DM
import qualified Data.Ord as DO
import qualified System.FilePath.Glob as Glob
import Test.QuickCheck (quickCheckAll)

-- frequency of characters
type Freq = DM.Map Char Integer

fromString :: String -> Freq
fromString = DM.fromListWith (+) . flip zip (repeat 1)

fromFile :: FilePath -> IO Freq
fromFile = fmap (fromString . DB.unpack) . DB.readFile

fromFiles :: [FilePath] -> IO Freq
fromFiles = fmap (DM.unionsWith (+)) . mapM fromFile

fromGlob :: FilePath -> String -> IO Freq
fromGlob fp = (=<<) fromFiles . flip Glob.globDir1 fp . Glob.compile

-- sum of relative frequencies of files
fromFilesRatio :: [FilePath] -> IO Freq
fromFilesRatio = fmap (DM.unionsWith (+)) . mapM (fmap ratio . fromFile)

-- sum of relative frequencies of files
fromGlobRatio :: FilePath -> String -> IO Freq
fromGlobRatio fp = (=<<) fromFilesRatio . flip Glob.globDir1 fp . Glob.compile

filterWith :: (Char -> Bool) -> Freq -> Freq
filterWith p = DM.filterWithKey (const . p)

sumTotal :: Freq -> Integer
sumTotal = DM.foldl' (+) 0

sumOf :: String -> Freq -> Integer
sumOf s = sumTotal . filterWith (`DL.elem` s)

-- relative
pct :: Freq -> DM.Map Char Float
pct freq = DM.map ((* 100) . (/ (fromIntegral $ sumTotal freq)) . fromIntegral) freq

-- relative
ratio :: Freq -> Freq
ratio = DM.map (round . (* 100)) . pct

ascii :: Freq -> Freq
ascii = filterWith DC.isAscii

unicase :: Freq -> Freq
unicase = DM.fromListWith (+) . map (CA.first DC.toLower) . DM.toList

printF :: Freq -> IO ()
printF = mapM_ print . DL.sortBy (flip $ DO.comparing snd) . DM.toList

prop_unicase s = unicase freq DM.! 'a' == sumOf "aA" freq where
    freq = fromString $ "aA" ++ s
prop_fiterWith s = freq == filterWith (`DL.elem` (DM.keys freq)) freq where
    freq = fromString s

return []
runTests = $quickCheckAll

-- > x <- fromGlob "./data" "**/*.txt"
-- > printF x
-- (' ',994534)
-- ('e',232929)
-- ('t',189974)
-- ...
