import 'package:flutter/material.dart';
import 'package:unveil_frontend/main.dart';
import 'package:unveil_frontend/services/Auth.dart'; // Make sure to import your AuthService

class LoginPage extends StatelessWidget {
  const LoginPage({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    final TextEditingController emailController = TextEditingController();
    final TextEditingController passwordController = TextEditingController();
    final AuthService authService = AuthService(); // Instantiate AuthService

    return Scaffold(
      body: Center(
        child: Padding(
          padding: const EdgeInsets.all(32.0), // Increased padding for web
          child: Container(
            decoration: BoxDecoration(
              color: Colors.white,
              borderRadius: BorderRadius.circular(16.0),
              boxShadow: [
                BoxShadow(
                  color: Colors.black.withOpacity(0.2),
                  spreadRadius: 4,
                  blurRadius: 20,
                  offset: const Offset(0, 4),
                ),
              ],
            ),
            padding: const EdgeInsets.all(32.0), // Increased padding for inner container
            child: Column(
              mainAxisAlignment: MainAxisAlignment.center,
              crossAxisAlignment: CrossAxisAlignment.stretch,
              children: [
                Text(
                  'Welcome Back',
                  style: TextStyle(
                    fontSize: 32, // Larger font size for web
                    fontWeight: FontWeight.bold,
                    color: Colors.black,
                  ),
                  textAlign: TextAlign.center,
                ),
                const SizedBox(height: 20.0),

                // Email Field
                TextField(
                  controller: emailController,
                  decoration: InputDecoration(
                    labelText: 'Email',
                    labelStyle: TextStyle(color: Colors.black54),
                    border: OutlineInputBorder(),
                    filled: true,
                    fillColor: const Color(0xFFF7F7F7), // Light gray background
                  ),
                  keyboardType: TextInputType.emailAddress,
                ),
                const SizedBox(height: 16.0),

                // Password Field
                TextField(
                  controller: passwordController,
                  decoration: InputDecoration(
                    labelText: 'Password',
                    labelStyle: TextStyle(color: Colors.black54),
                    border: OutlineInputBorder(),
                    filled: true,
                    fillColor: const Color(0xFFF7F7F7), // Light gray background
                  ),
                  obscureText: true,
                ),
                const SizedBox(height: 20.0),

                // Login Button
                ElevatedButton(
                  onPressed: () async {
                    final email = emailController.text;
                    final password = passwordController.text;

                    // Call the AuthService login method
                    bool success = await authService.login(email, password);
                    
                    if (success) {
                      // Handle successful login, navigate to the next page
                      print('Login successful');
                      // Navigate to the home page or dashboard
                    } else {
                      // Handle login failure, show a message
                      print('Login failed');
                      ScaffoldMessenger.of(context).showSnackBar(
                        SnackBar(content: Text('Login failed. Please try again.')),
                      );
                    }
                  },
                  style: ElevatedButton.styleFrom(
                    foregroundColor: Colors.white,
                    backgroundColor: Colors.black,
                    padding: const EdgeInsets.symmetric(vertical: 16.0), // White text color
                    shape: RoundedRectangleBorder(
                      borderRadius: BorderRadius.circular(8.0),
                    ),
                  ),
                  child: const Text(
                    'Login',
                    style: TextStyle(fontSize: 16),
                  ),
                ),
                const SizedBox(height: 16.0),

                // Sign Up Link
                TextButton(
                  onPressed: () {
                  
                    // Navigate to sign up page (implement navigation logic)
                    print('Navigate to Sign Up');
                  },
                  child: const Text(
                    "Don't have an account? Sign Up",
                    style: TextStyle(color: Colors.black54),
                  ),
                ),
              ],
            ),
          ),
        ),
      ),
    );
  }
}
