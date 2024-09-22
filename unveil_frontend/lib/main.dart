import 'package:flutter/material.dart';
import 'package:unveil_frontend/pages/UploadArt.dart';
import 'package:unveil_frontend/pages/account.dart';
import 'package:unveil_frontend/pages/viewArtWork.dart';
import 'package:unveil_frontend/widgets/minimalnavbar.dart';

void main() {
  runApp(const ArtGalleryApp());
}

class ArtGalleryApp extends StatelessWidget {
  const ArtGalleryApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      theme: ThemeData(
        brightness: Brightness.light,
        scaffoldBackgroundColor: Colors.white,
        appBarTheme: const AppBarTheme(
          backgroundColor: Colors.transparent,
          elevation: 0,
          iconTheme: IconThemeData(color: Colors.black),
          titleTextStyle: TextStyle(
            color: Colors.black,
            fontSize: 20,
            fontWeight: FontWeight.w300,
          ),
        ),
        textTheme: const TextTheme(
          bodySmall: TextStyle(color: Colors.black),
        ),
        buttonTheme: ButtonThemeData(
          textTheme: ButtonTextTheme.normal,
          buttonColor: Colors.black,
        ),
      ),
      darkTheme: ThemeData(
        brightness: Brightness.dark,
        scaffoldBackgroundColor: Colors.black,
        appBarTheme: const AppBarTheme(
          backgroundColor: Colors.transparent,
          elevation: 0,
          iconTheme: IconThemeData(color: Colors.white),
          titleTextStyle: TextStyle(
            color: Colors.white,
            fontSize: 20,
            fontWeight: FontWeight.w300,
          ),
        ),
        textTheme: const TextTheme(
          bodySmall: TextStyle(color: Colors.white),
          bodyMedium: TextStyle(color: Colors.white),
        ),
        buttonTheme: ButtonThemeData(
          textTheme: ButtonTextTheme.normal,
          buttonColor: Colors.white,
        ),
      ),
      themeMode: ThemeMode.system,
      home: const MainView(),
    );
  }
}

class MainView extends StatefulWidget {
  const MainView({super.key});

  @override
  State<MainView> createState() => _MainViewState();
}

class _MainViewState extends State<MainView> {
  int currentIndex = 0;

 final List<Widget> pages = [
   const ViewArt(),
  const UploadArt(),
  const Account(),
];

  final List<String> navItems = ['View', 'Upload', 'Account'];

  void _onPageSelected(int index) {
    setState(() {
      currentIndex = index;
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
      ),
      body: pages[currentIndex], // Display the selected page
      bottomNavigationBar: MinimalNavBar(
        items: navItems,
        selectedIndex: currentIndex,
        onItemSelected: _onPageSelected,
        locations: pages, // Pass the pages list here
      ),
    );
  }
}
