# dawg.py

class Dawg:
    def pathToLetter(node, char: str):
        """
        Returns the edge that leads to a node given the character.
        If the edge doesn't exist, None is returned.
        """
        foundEdges = [edge for edge in node.outgoingEdges if edge.value == char]
        return foundEdges[0] if foundEdges else None

    def __init__(self):
        self.root = DawgNode(0)  # Root node
        self.nodes = [self.root]  # List of all nodes
        self.edges = []
        self.genre_song_counts = {}  # Dictionary to store counts

        # Assign weights to subsets
        self.subset_weights = {
            "Top Artists": 1.1,
            "Saved Albums": 1.3,
            "Saved Tracks": 1.5,
            "Top Tracks": 1.7,
            "Recently Played": 1.9
        }

    def load_from_spotify_data(self, song_hierarchy):
        """
        Takes the song hierarchy built from Spotify data and integrates it into the graph structure.
        """
        print("Adding song hierarchies to DAWG")

        for genre, subsets in song_hierarchy.items():
            self.addGenreToDawg(genre, subsets)

        print("DAWG initialization complete")

    def getStartNode(self):
        return self.root  # Root node

    def addGenreToDawg(self, genre, subsets):
        """
        Adds a genre to the DAWG structure, followed by its subsets (top artists, saved albums, etc.).
        """
        currentNode = self.root
        # Add genre level to DAWG
        for char in genre.lower():
            edge = Dawg.pathToLetter(currentNode, char)
            if edge:
                currentNode = edge.to
            else:
                newNode = DawgNode(currentNode.curWordLength + 1)
                currentNode.connectEdgeTo(newNode, char)
                currentNode = newNode

        currentNode.isGenre = True
        genreNode = currentNode  # Keep a reference to the genre node

        # Initialize the song count dictionary for this genre
        if genre not in self.genre_song_counts:
            self.genre_song_counts[genre] = {}

        # Now add subsets under this genre
        for subset_name, songs in subsets.items():
            subsetNode = self.addSubsetToDawg(subset_name, genreNode)
            weight = self.subset_weights.get(subset_name, 1)  # Default weight is 1 if not specified
            # Add songs under this subset
            for song in songs:
                self.addSongToDawg(song, subsetNode)
                # Update the song count with the weight
                if song in self.genre_song_counts[genre]:
                    self.genre_song_counts[genre][song] += weight
                else:
                    self.genre_song_counts[genre][song] = weight

    def addSubsetToDawg(self, subset_name, parentNode):
        """
        Adds a subset (like Top Artists, Saved Albums) under a given parent node (genre or higher subset).
        """
        currentNode = parentNode
        # Add subset level to DAWG
        for char in subset_name.lower():
            edge = Dawg.pathToLetter(currentNode, char)
            if edge:
                currentNode = edge.to
            else:
                newNode = DawgNode(currentNode.curWordLength + 1)
                currentNode.connectEdgeTo(newNode, char)
                currentNode = newNode
        currentNode.isSubset = True
        return currentNode

    def addSongToDawg(self, song, parentNode):
        """
        Adds a song name to the DAWG structure under a given subset node.
        """
        currentNode = parentNode
        # Add song level to DAWG
        for char in song.lower():
            edge = Dawg.pathToLetter(currentNode, char)
            if edge:
                currentNode = edge.to
            else:
                newNode = DawgNode(currentNode.curWordLength + 1)
                currentNode.connectEdgeTo(newNode, char)
                currentNode = newNode

        currentNode.isWord = True  # Mark the node as a word (song)

    def findSong(self, genre: str, song: str):
        """
        Searches for a song in a specific genre, traversing through subsets if the genre is found.
        """
        print(f"\nSearching for song '{song}' in genre '{genre}'")
        # First, find the genre node
        genreNode = self.getNodeByPath(self.root, genre.lower())
        if not genreNode or not genreNode.isGenre:
            print(f"Genre '{genre}' not found.\n")
            return False

        # Now, search through subsets under the genre node
        found = False
        for edge in genreNode.outgoingEdges:
            subsetNode = edge.to
            if subsetNode.isSubset:
                songNode = self.getNodeByPath(subsetNode, song.lower())
                if songNode and songNode.isWord:
                    subsetName = self.getPathToNode(subsetNode, genreNode)
                    print(f"Found song '{song}' in genre '{genre}' under subset '{subsetName}'.\n")
                    found = True
                    break
        if not found:
            print(f"Song '{song}' not found in genre '{genre}'.\n")
        return found

    def getNodeByPath(self, startNode, pathStr):
        """
        Traverses the DAWG from the startNode using the pathStr and returns the final node.
        """
        currentNode = startNode
        for char in pathStr:
            edge = Dawg.pathToLetter(currentNode, char)
            if edge:
                currentNode = edge.to
            else:
                return None
        return currentNode

    def getPathToNode(self, node, rootNode):
        """
        Returns the path (string) from the rootNode to the given node.
        """
        path = ''
        currentNode = node
        while currentNode != rootNode and currentNode.incomingEdges:
            edge = currentNode.incomingEdges[0]  # Assuming single parent for simplicity
            path = edge.value + path
            currentNode = edge.previous
        return path

    def getGenreSongCounts(self):
        """
        Returns the genre song counts dictionary.
        """
        return self.genre_song_counts

class DawgNode:
    def __init__(self, curWordLength=None):
        self.curWordLength = curWordLength if curWordLength else 0
        self.incomingEdges = []  # Edges coming into this node
        self.outgoingEdges = []  # Edges going out from this node
        self.isGenre = False     # Indicates if the node represents a genre
        self.isSubset = False    # Indicates if the node represents a subset
        self.isWord = False      # Indicates if the current node is the end of a word (song name)

    def connectEdgeTo(self, node2, value):
        edgeRef = DawgEdge(value, self, node2)
        self.outgoingEdges.append(edgeRef)
        node2.incomingEdges.append(edgeRef)

class DawgEdge:
    def __init__(self, value=None, from_=None, to=None):
        self.value = value
        self.to = to
        self.previous = from_

    def __str__(self):
        return self.value
