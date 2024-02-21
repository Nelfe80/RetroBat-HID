I created a small program called GunRPointer to play shooting games with a mouse, tested on the PlayStation (PSX) Retroarch Libreto Emulator. The principle of the program is to detect the position of the mouse pointer and gradually force it to move towards the center of the screen. This method allows simulating gamepad movements using a mouse. This technique is particularly useful for playing shooting games with guns that emulate the mouse's position on the screen, which was the initial objective of the program.

GunRPointer was tested with the game "Medal of Honor" on PSX, launched through Retrobat, a software for playing retro games. The right-click function of the mouse is set to enter a targeting mode in the game, enabling players to aim at enemies. Moving the mouse or the gun upwards makes the character advance, and moving it downwards causes the character to retreat. However, for movement within the game, it's preferable to use the gamepad or the directional keys (up, down, left, right). This setup provides a novel way to experience classic shooting games on the PSX using modern input devices like the mouse and guns.

Additionally, it's important to note that using GunRPointer does not require any modification or hacking of the game ROM. There is no need for any complex setup or alteration of the game files. To use the program, you simply need to run the GunRPointer executable file (".exe"). This straightforward approach allows for an easy and accessible way to enhance the gaming experience, particularly for shooting games, without the technical challenges of modifying game data.

To play "Medal of Honor" on PSX
In RETROBAT, in system, uncheck automap gamepad option. (or map keyboard L2 to d et R2 to e)
In the file emulators/retroarch/retroarch.cfg, please add or change :
input_player1_l2 = "d"
input_player1_r2 = "e"

Please test it on others games and send me your comments and videos


----


J'ai créé un petit programme nommé GunRPointer pour jouer aux jeux de tir avec une souris, testé sur l'émulateur PlayStation (PSX) Retroarch Libreto. Le principe du programme est de détecter la position du curseur de la souris et de le forcer progressivement à se déplacer vers le centre de l'écran. Cette méthode permet de simuler les mouvements d'un gamepad avec une souris. Cette technique est particulièrement utile pour jouer à des jeux de tir avec des armes qui émulent la position de la souris sur l'écran, ce qui était l'objectif initial du programme.

GunRPointer a été testé avec le jeu "Medal of Honor" sur PSX, lancé via Retrobat, un logiciel pour jouer à des jeux rétro. La fonction de clic droit de la souris est configurée pour entrer en mode de ciblage dans le jeu, permettant aux joueurs de viser les ennemis. Déplacer la souris ou l'arme vers le haut fait avancer le personnage, et vers le bas le fait reculer. Cependant, pour se déplacer dans le jeu, il est préférable d'utiliser le gamepad ou les touches directionnelles (haut, bas, gauche, droite). Cette configuration offre une nouvelle façon de vivre l'expérience des jeux de tir classiques sur PSX en utilisant des dispositifs d'entrée modernes comme la souris et les armes.

De plus, il est important de noter que l'utilisation de GunRPointer ne nécessite aucune modification ou hack de la ROM du jeu. Aucune configuration complexe ou altération des fichiers de jeu n'est nécessaire. Pour utiliser le programme, il suffit de lancer le fichier exécutable GunRPointer (".exe"). Cette approche simple permet une manière facile et accessible d'améliorer l'expérience de jeu, en particulier pour les jeux de tir, sans les défis techniques de modifier les données du jeu.

Pour jouer à "Medal of Honor" sur PSX
Dans RETROBAT, dans le système, décochez l'option d'automatisation du gamepad (ou associez le L2 du clavier à d et le R2 à e).
Dans le fichier emulators/retroarch/retroarch.cfg, veuillez ajouter ou modifier :
input_player1_l2 = "d"
input_player1_r2 = "e"

Merci de tester cela sur d'autres jeux et de m'envoyer vos commentaires et vidéos.