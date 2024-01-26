
(configuration
  :background-image "/home/silvio/Pictures/BlindMansRampage/Game1/Floor1/BlindManFloor1_DEBUG.png")

(spaces
  (upper-shop (120 90))
  (upper-unlucky (334 66))
  (upper-right-gray-1 (498 61))
  (upper-right-gray-2 (627 65))
  (upper-lucky (373 149))
  (star (511 144))
  (left-gray-1 (133 229))
  (left-gray-2 (262 224))
  (library (512 236))
  (start (220 327))
  (center-gray (364 327))
  (lower-left-lucky (319 410))
  (lower-center-gray (442 412))
  (lower-unlucky (547 412))
  (lower-shop (204 464))
  (lower-gray-1 (351 476))
  (lower-gray-2 (485 487))
  (lower-right-lucky (606 486))
  (lower-left-gray (217 530))
  (bowser (484 560)))

(objects
  (object star "/home/silvio/Documents/star.png" upper-shop)
  (object star1 "/home/silvio/Documents/star.png" start)
  (object mercerenies "discord:87351108317491200" start))

(commands
  (move mercerenies center-gray))
