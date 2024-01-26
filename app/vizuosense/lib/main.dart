import 'package:flutter/material.dart';
// Main.dart application code

void main() {
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({Key? key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Flutter Demo',
      theme: ThemeData(
        primarySwatch: Colors.blue,
      ),
      home: MyHomePage(title: 'VizuoSense'),
    );
  }
}

class MyHomePage extends StatefulWidget {
  const MyHomePage({Key? key, required this.title}) : super(key: key);

  final String title;

  @override
  _MyHomePageState createState() => _MyHomePageState();
}

class _MyHomePageState extends State<MyHomePage> {
  String prompt = ''; // Variable to store the text prompt
  TextEditingController _textEditingController = TextEditingController();
  List<Widget> chatMessages = []; // List to store chat messages
  String imageUrl = ''; // Variable to store the uploaded image URL

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text(widget.title),
        centerTitle: true,
        actions: [
          IconButton(
            icon: const Icon(Icons.settings),
            onPressed: () {
              // Handle settings button press
            },
          ),
        ],
      ),
      body: Column(
        children: [
          Expanded(
            child: ListView(
              reverse: true,
              children: chatMessages,
            ),
          ),
          Padding(
            padding: const EdgeInsets.all(8.0),
            child: Row(
              children: [
                Expanded(
                  child: _buildImageInput(),
                ),
                IconButton(
                  icon: Icon(Icons.send),
                  onPressed: () {
                    // Handle sending message
                    String message = _textEditingController.text;
                    if (message.isNotEmpty || imageUrl.isNotEmpty) {
                      // Add the user's message to the chat list
                      setState(() {
                        _textEditingController.clear();
                        _addImageMessage(); // Add image message
                        _addChatMessage(message, isUser: true);
                      });
                    }
                  },
                ),
              ],
            ),
          ),
        ],
      ),
    );
  }

  // Helper method to build the image input UI
  Widget _buildImageInput() {
    return Column(
      children: [
        imageUrl.isEmpty
            ? GestureDetector(
                onTap: () {
                  // Handle image upload here
                  _addImageMessage(); // For demo, consider this as image upload
                },
                child: Container(
                  padding: EdgeInsets.all(16.0),
                  decoration: BoxDecoration(
                    color: Color.fromARGB(255, 247, 247, 247),
                    borderRadius: BorderRadius.circular(8.0),
                  ),
                  child: Column(
                    children: [
                      Icon(Icons.image, size: 50, color: Colors.grey),
                      SizedBox(height: 8.0),
                      Text(
                        'Upload an image',
                        style: TextStyle(color: Colors.grey),
                      ),
                    ],
                  ),
                ),
              )
            : Image.network(imageUrl),
        const SizedBox(height: 8.0),
        TextField(
          controller: _textEditingController,
          enabled: imageUrl.isNotEmpty, // Enable only if image is uploaded
          decoration: InputDecoration(
            hintText: 'Type your message...',
            border: OutlineInputBorder(),
          ),
        ),
      ],
    );
  }

  // Helper method to add an image message to the list
  void _addImageMessage() {
    // ... (previous image message logic remains the same)

    // Update the UI to enable the "Send" button
    setState(() {
      imageUrl =
          'https://example.com/sample-image.jpg'; // Replace with actual image URL
    });
  }

  // Helper method to add a chat message to the list
  void _addChatMessage(String message, {bool isUser = false}) {
    // ... (previous method content remains the same)
  }
}
