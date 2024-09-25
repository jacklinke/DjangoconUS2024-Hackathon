import 'package:flutter/material.dart';
import 'package:unveil_frontend/pages/UploadArt.dart';
import 'package:unveil_frontend/pages/account.dart';
import 'package:unveil_frontend/pages/viewArtWork.dart';
import 'package:unveil_frontend/pages/login.dart'; // Import your Login page
import 'package:unveil_frontend/pages/signup.dart'; // Import your Sign-up page
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
      themeMode: ThemeMode.light,
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
  bool isAuthenticated = false; // Add authentication state

  final List<Widget> authPages = [
    const ViewArt(),
    const UploadArt(),
    Account(),
  ];

  final List<Widget> unauthPages = [
    const LoginPage(), // Your login page widget
    const SignUpPage(), // Your sign-up page widget
  ];

  final List<String> navItemsAuthenticated = ['View', 'Upload', 'Account'];
  final List<String> navItemsUnauthenticated = ['Login', 'Sign Up'];

  void _onPageSelected(int index) {
    setState(() {
      currentIndex = index;
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(),
      body: isAuthenticated 
          ? authPages[currentIndex] // Display the authenticated pages
          : unauthPages[currentIndex], // Display the unauthenticated pages
      bottomNavigationBar: BottomNavigationBar(
        items: isAuthenticated 
            ? navItemsAuthenticated.map((item) => BottomNavigationBarItem(icon: const Icon(Icons.art_track), label: item)).toList()
            : navItemsUnauthenticated.map((item) => BottomNavigationBarItem(icon: const Icon(Icons.login), label: item)).toList(),
        currentIndex: currentIndex,
        onTap: (index) {
          if (isAuthenticated || index < 2) { // Only allow navigation for unauthenticated to login/signup
            _onPageSelected(index);
          }
        },
      ),
    );
  }
}


