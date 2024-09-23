import 'package:flutter/material.dart';

class ViewArt extends StatefulWidget {
  const ViewArt({Key? key}) : super(key: key);

  @override
  _ViewArtState createState() => _ViewArtState();
}

class _ViewArtState extends State<ViewArt> {
  // List of artworks
  final List<Map<String, String>> artworks = [
    {
      'title': 'Artwork 1',
      'description': 'This is a description of Artwork 1.',
      'image': 'https://picsum.photos/400/600?random=1',
    },
    {
      'title': 'Artwork 2',
      'description': 'This is a description of Artwork 2.',
      'image': 'https://picsum.photos/400/600?random=2',
    },
    {
      'title': 'Artwork 3',
      'description': 'This is a description of Artwork 3.',
      'image': 'https://picsum.photos/400/600?random=3',
    },
  ];

  int currentIndex = 0;

  // Method to go to the next artwork
  void _nextArtwork() {
    setState(() {
      currentIndex = (currentIndex + 1) % artworks.length; // Loop back to start
    });
  }

  // Method to go to the previous artwork
  void _previousArtwork() {
    setState(() {
      currentIndex = (currentIndex - 1 + artworks.length) % artworks.length; // Loop back to end
    });
  }

  @override
  Widget build(BuildContext context) {
    final isMobile = MediaQuery.of(context).size.width < 600;

    return Scaffold(
      body: LayoutBuilder(
        builder: (context, constraints) {
          final width = constraints.maxWidth;

          return Center(
            child: Column(
              mainAxisAlignment: MainAxisAlignment.center,
              children: [
                Row(
                  mainAxisAlignment: MainAxisAlignment.center,
                  children: [
                    // Left side button for Previous
                    GestureDetector(
                      onTap: _previousArtwork,
                      child: Container(
                        width: 80, // Adjust width for how big the button should be
                        height: isMobile ? width * 0.7 : 600, // Same height as the image
                        color: Colors.grey[300], // Gray background
                        child: const Icon(
                          Icons.arrow_back_ios,
                          size: 50,
                          color: Colors.black,
                        ),
                      ),
                    ),
                    const SizedBox(width: 10),
                    // Image container
                    Container(
                      width: isMobile ? width * 0.8 : 500, // Adjust width for larger images
                      height: isMobile ? width * 0.7 : 600, // Adjust height for larger images
                      decoration: BoxDecoration(
                        border: Border.all(
                          color: Theme.of(context).brightness == Brightness.dark
                              ? Colors.white
                              : Colors.black,
                          width: 1,
                        ),
                      ),
                      child: Image.network(
                        artworks[currentIndex]['image']!,
                        fit: BoxFit.cover,
                        loadingBuilder: (context, child, loadingProgress) {
                          if (loadingProgress == null) {
                            return child;
                          }
                          return const Center(
                            child: CircularProgressIndicator(),
                          );
                        },
                        errorBuilder: (context, error, stackTrace) {
                          return Center(
                            child: Text(
                              'Image not available',
                              style: TextStyle(
                                color: Theme.of(context).brightness == Brightness.dark
                                    ? Colors.white
                                    : Colors.black,
                              ),
                            ),
                          );
                        },
                      ),
                    ),
                    const SizedBox(width: 10),
                    // Right side button for Next
                    GestureDetector(
                      onTap: _nextArtwork,
                      child: Container(
                        width: 80, // Adjust width for how big the button should be
                        height: isMobile ? width * 0.7 : 600, // Same height as the image
                        color: Colors.grey[300], // Gray background
                        child: const Icon(
                          Icons.arrow_forward_ios,
                          size: 50,
                          color: Colors.black,
                        ),
                      ),
                    ),
                  ],
                ),
                const SizedBox(height: 20),
                Padding(
                  padding: EdgeInsets.symmetric(horizontal: isMobile ? 20 : 0),
                  child: Text(
                    artworks[currentIndex]['title']!,
                    style: TextStyle(
                      fontSize: isMobile ? 20 : 24,
                      fontWeight: FontWeight.w300,
                      color: Theme.of(context).brightness == Brightness.dark
                          ? Colors.white
                          : Colors.black,
                    ),
                    textAlign: TextAlign.center,
                  ),
                ),
                const SizedBox(height: 10),
                Padding(
                  padding: EdgeInsets.symmetric(horizontal: isMobile ? 20 : 0),
                  child: Text(
                    artworks[currentIndex]['description']!,
                    style: TextStyle(
                      fontSize: isMobile ? 14 : 16,
                      fontWeight: FontWeight.w300,
                      color: Theme.of(context).brightness == Brightness.dark
                          ? Colors.white
                          : Colors.black,
                    ),
                    textAlign: TextAlign.center,
                  ),
                ),
              ],
            ),
          );
        },
      ),
    );
  }
}
