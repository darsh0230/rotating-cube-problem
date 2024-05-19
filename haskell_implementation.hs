import Graphics.Gloss
import Graphics.Gloss.Interface.Pure.Game
import System.Random (StdGen, newStdGen, randomR)
-- import System.Exit (exitSuccess)

type Angle = Float
type Point3D = (Float, Float, Float)
type Line = (Point3D, Point3D)
type Pos = (Float, Float)
type LineFunc = [Point3D] -> [Line]

-- Define cube vertices for a cube centered at the origin
cubeVertices :: [Point3D]
cubeVertices = 
    [
      (-60,  60, -60)
    , ( 60,  60, -60)
    , ( 60,  60,  60)
    , (-60,  60,  60)
    , (-60, -60, -60)
    , ( 60, -60, -60)
    , ( 60, -60,  60)
    , (-60, -60,  60)
    ]


-- Define cube edges from its vertices
cubeEdges :: [Point3D] -> [Line]
cubeEdges vertices = [ (vertices !! 0, vertices !! 1), (vertices !! 1, vertices !! 2),
                       (vertices !! 2, vertices !! 3), (vertices !! 3, vertices !! 0),
                       (vertices !! 4, vertices !! 5), (vertices !! 5, vertices !! 6),
                       (vertices !! 6, vertices !! 7), (vertices !! 7, vertices !! 4),
                       (vertices !! 0, vertices !! 4), (vertices !! 1, vertices !! 5),
                       (vertices !! 2, vertices !! 6), (vertices !! 3, vertices !! 7) ]


tetrahedronVertices :: [Point3D]
tetrahedronVertices = 
    [
      ( 60,  60,  60)
    , ( 60, -60, -60)
    , (-60,  60, -60)
    , (-60, -60,  60) 
    ]

tetrahedronEdges :: [Point3D] -> [Line]
tetrahedronEdges v = 
    [
        (v !! 0, v !! 1),
        (v !! 1, v !! 2),
        (v !! 2, v !! 0),
        (v !! 0, v !! 3),
        (v !! 1, v !! 3),
        (v !! 2, v !! 3)
    ]

octahedronVertices :: [Point3D]
octahedronVertices = 
    [
     ( 60,   0,   0),
     (-60,   0,   0),
     (  0,  60,   0),
     (  0, -60,   0),
     (  0,   0,  60),
     (  0,   0, -60)
    ]

octahedronEdges :: [Point3D] -> [Line]
octahedronEdges v =
    [
        (v !! 3, v !! 1),
        (v !! 3, v !! 0),
        (v !! 3, v !! 4),
        (v !! 3, v !! 5),
        (v !! 2, v !! 1),
        (v !! 2, v !! 0),
        (v !! 2, v !! 4),
        (v !! 2, v !! 5),
        (v !! 5, v !! 1),
        (v !! 5, v !! 0),
        (v !! 4, v !! 1),
        (v !! 4, v !! 0)
    ]


dodecahedronVertices :: [Point3D]
dodecahedronVertices = 
    [
        (-55, -55, 55),
        (0, -89, -34),
        (-55, -55, -55),
        (-89, -34, 0),
        (-34, 0, -89),
        (-55, 55, 55),
        (0, 89, -34),
        (34, 0, -89),
        (-55, 55, -55),
        (0, -89, 34),
        (-89, 34, 0),
        (-34, 0, 89),
        (89, 34, 0),
        (89, -34, 0),
        (55, 55, 55),
        (55, -55, 55),
        (34, 0, 89),
        (55, -55, -55),
        (55, 55, -55),
        (0, 89, 34)
    ]

dodecahedronEdges :: [Point3D] -> [Line]
dodecahedronEdges v = 
    [
        (v !! 11, v !! 16), (v !! 4, v !! 7), (v !! 13, v !! 15), (v !! 13, v !! 12), (v !! 13, v !! 17), (v !! 12, v !! 14), (v !! 12, v!! 18), (v !! 17, v!! 7), (v !! 18, v !! 7), (v !! 15, v !! 16), (v !! 14, v !! 16), (v !! 3, v !! 0), (v !! 3, v !! 10), (v !! 3, v !! 2), (v !! 
            10, v !! 5), (v !! 10, v !! 8), (v !! 2, v !! 4), (v !! 8, v !! 4), (v !! 0, v !! 11), (v !! 5, v !! 11), (v !! 19, v !! 5), (v !! 19, v !! 14), (v !! 19, v !! 6), (v !! 6, v !! 8), (v !! 6, v !! 18), (v !! 9, v !! 0), (v !! 9, v !! 15), (v !! 9, v !! 1), (v !! 1, v !! 2), (v !! 1, v !! 17)
    ]


translateXY :: (Float, Float) -> Point3D -> Point3D
translateXY (x', y') (x, y, z) = (x + x', y + y', z)

-- Rotate a point around the x-axis
rotateX :: Angle -> Point3D -> Point3D
rotateX theta (x, y, z) =
    let y' = y * cos theta - z * sin theta
        z' = y * sin theta + z * cos theta
    in (x, y', z')

-- Rotate a point around the y-axis
rotateY :: Angle -> Point3D -> Point3D
rotateY theta (x, y, z) =
    let x' = x * cos theta - z * sin theta
        z' = x * sin theta + z * cos theta
    in (x', y, z')

-- Rotate a point around the z-axis
rotateZ :: Angle -> Point3D -> Point3D
rotateZ theta (x, y, z) =
    let x' = x * cos theta - y * sin theta
        y' = x * sin theta + y * cos theta
    in (x', y', z)


thickLine :: Point -> Point -> Float -> Picture
thickLine (x1, y1) (x2, y2) thickness = Polygon [ (x1', y1'), (x2', y2'), (x2'', y2''), (x1'', y1'') ]
  where
    angle = atan2 (y2 - y1) (x2 - x1)
    dx = thickness / 2 * cos (angle + pi / 2)
    dy = thickness / 2 * sin (angle + pi / 2)
    (x1', y1') = (x1 + dx, y1 + dy)
    (x2', y2') = (x2 + dx, y2 + dy)
    (x1'', y1'') = (x1 - dx, y1 - dy)
    (x2'', y2'') = (x2 - dx, y2 - dy)

-- Display the cube
renderCube :: [Line] -> Picture
renderCube = Pictures . map renderLine
    where
        renderLine :: Line -> Picture
        renderLine ((x1, y1, z1), (x2, y2, z2)) =
            Color white $ thickLine (x1, y1) (x2, y2) 3

-- Define the state of the game
data GameState = GameState
    { cubes     :: [(Pos, LineFunc, [Point3D])]
    , angleX    :: Angle
    , angleY    :: Angle
    , angleZ    :: Angle
    , rotating  :: Bool
    , direction :: Float
    , speed     :: Float
    , rng       :: StdGen
    }

-- Initial state
initialState :: StdGen -> GameState
initialState gen = GameState [((0.0, 0.0), cubeEdges, cubeVertices)] 0 0 0 True 1 1 gen
    -- where createCube pos = let verts = cubeVertices pos in (verts, cubeEdges verts)

-- Handle input
handleInput :: Event -> GameState -> GameState
handleInput (EventKey (Char 's') Down _ _)           state = state { rotating = not (rotating state) }
handleInput (EventKey (Char 'r') Down _ _)           state = state { direction = -direction state }
handleInput (EventKey (SpecialKey KeyUp) Down _ _)   state = state { speed = speed state + 0.1 }
handleInput (EventKey (SpecialKey KeyDown) Down _ _) state = state { speed = max 0 (speed state - 0.1) }
handleInput (EventKey (Char '1') Down _ _)           state = addRandomCube   state
handleInput (EventKey (Char '2') Down _ _)           state = addTertahedron  state
handleInput (EventKey (Char '3') Down _ _)           state = addOctahedron   state
handleInput (EventKey (Char '4') Down _ _)           state = addDodecahedron state
handleInput (EventKey (Char 'd') Down _ _)           state = removeLastCube  state
-- handleInput (EventKey (Char 'q') Down _ _)            _    = exitSuccess
handleInput _ state = state

-- Update the state
update :: Float -> GameState -> GameState
update deltaTime state
    | rotating state = state { angleX = angleX state + direction state * speed state * deltaTime
                             , angleY = angleY state + direction state * speed state * deltaTime
                             , angleZ = angleZ state + direction state * speed state * deltaTime
                             }
    | otherwise = state

-- Draw the state
draw :: GameState -> Picture
draw state = Pictures $ map (renderCube . transformObj) (cubes state)
    where
        transformObj (pos, lineFunc, vertices) = lineFunc transformedVeritces
            where transformedVeritces = map (translateXY pos . rotateX (angleX state) . rotateY (angleY state) . rotateZ (angleZ state)) vertices


addRandomCube :: GameState -> GameState
addRandomCube state = 
    let (x, gen1) = randomR (-300, 300) (rng state)
        (y, _)    = randomR (-300, 300) gen1
        newCube = ((x, y), cubeEdges, cubeVertices)
    in state {cubes = newCube : cubes state, rng = gen1}

addTertahedron :: GameState -> GameState
addTertahedron state = 
    let (x, gen1) = randomR (-300, 300) (rng state)
        (y, _)    = randomR (-300, 300) gen1
        newObj = ((x, y), tetrahedronEdges, tetrahedronVertices)
    in state {cubes = newObj : cubes state, rng = gen1}

addOctahedron :: GameState -> GameState
addOctahedron state = 
    let (x, gen1) = randomR (-300, 300) (rng state)
        (y, _)    = randomR (-300, 300) gen1
        newObj = ((x, y), octahedronEdges, octahedronVertices)
    in state {cubes = newObj : cubes state, rng = gen1}

addDodecahedron :: GameState -> GameState
addDodecahedron state = 
    let (x, gen1) = randomR (-300, 300) (rng state)
        (y, _)    = randomR (-300, 300) gen1
        newObj = ((x, y), dodecahedronEdges, dodecahedronVertices)
    in state {cubes = newObj : cubes state, rng = gen1}

-- Remove the last added cube
removeLastCube :: GameState -> GameState
removeLastCube state = state { cubes = if null (cubes state) then [] else init (cubes state) }


-- Main function to display the rotating cube
main :: IO ()
main = do
    gen <- newStdGen
    play (InWindow "Rotating Cube" (1280, 720) (10, 10)) black 60 (initialState gen) draw handleInput update



