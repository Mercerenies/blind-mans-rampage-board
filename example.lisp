
;; This is an example input file for the Blind Man's Rampage video
;; renderer. Your input file must consist of four S-expressions in the
;; same order as this file: configuration, spaces, objects, commands.
;;
;; All relative file paths in an input file are resolved relative to
;; the input file itself, NOT to the working directory from which the
;; program was run.

;; The configuration object describes basic global configuration data
;; about the resulting video. The configuration object consists of
;; key-value pairs, where each key is a symbol beginning with a colon.
(configuration
  ;; background-image (required) indicates the image to use as the
  ;; background for the board. This is drawn behind all objects before
  ;; each frame. This also determines the size of the canvas.
  ;;
  ;; It is recommended that the dimensions of this image be a multiple
  ;; of 16, and it is recommended that a bit of blank space be left at
  ;; the bottom, to allow text to be drawn without covering up other
  ;; content.
  ;;
  ;; This must be a file path. It cannot be a Discord user ID.
  :background-image "Background.png"
  ;; fps (optional) is the frames per second of the video. Default
  ;; value is 60.
  :fps 60
  ;; start-space (optional) is a symbol representing the name of the
  ;; starting space. If not provided, defaults to the word "start".
  :start-space start)

;; This mapping determines where the spaces are located on the board.
;; Each position in this mapping shall be a pair (x y) of coordinates,
;; where (0 0) is the top-left corner of the canvas. The start space
;; named in configuration MUST be present in this mapping.
(spaces
  (shop (120 90))
  (start (220 327)))

;; The objects initially present in the game room. Each object must be
;; of the form
;;
;; (object name image-path start-space)
;;
;; Where the image path can either be a local file path or the string
;; "discord:" followed by a Discord user ID. In the latter case, the
;; Discord user's avatar will be retrieved as the image.
(objects
  (object star "Star.png" shop)
  (object discord-user "discord:00000000000000000" start))

;; The commands will run in sequence and perform the actual animation
;; work. All command types are listed below.
(commands
  ;; (move player-name space-name)
  ;;
  ;; Moves an object to the given space.
  (move discord-user shop)
  ;; (swap player1 player2)
  ;;
  ;; Swaps two objects' positions.
  (swap discord-user star)
  ;; (shuffle (player1 player2) ...)
  ;;
  ;; Generalized swap command. For each sub-list, moves player1 to the
  ;; position of player2. Movements happen simultaneously.
  (shuffle
    (discord-user star)
    (star discord-user))
  ;; (add name image-path start-space)
  ;;
  ;; Adds a new object to the game board. Parameters are interpreted
  ;; the same as the (object ...) starting form.
  (add sparky "Sparky.png" shop)
  ;; (remove name)
  ;;
  ;; Removes an object from the game board.
  (remove sparky)
  ;; (change-background image-path)
  ;;
  ;; Fades to a new background image. The new background image must
  ;; have the same width and height as the original.
  (change-background "Background1.png")
  ;; (text string)
  ;;
  ;; Shows the given text at the bottom of the screen. Text is shown
  ;; instantaneously and remains until replaced or hidden.
  (text "Things happened!")
  ;; (hide-text)
  ;;
  ;; Hides any displayed bottom text.
  (hide-text)
  ;; (title string)
  ;;
  ;; Shows the given text at the top of the screen. Text is shown
  ;; instantaneously and remains until replaced or hidden.
  (title "The Game")
  ;; (hide-title)
  ;;
  ;; Hides any displayed title text.
  (hide-title)
  ;; (wait frames)
  ;;
  ;; Do nothing for the specified amount of time.
  (wait 30))
