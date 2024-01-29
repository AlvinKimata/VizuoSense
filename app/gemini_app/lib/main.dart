import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:camera/camera.dart';
import 'package:dio/dio.dart';
import 'package:flutter_tts/flutter_tts.dart';
import 'package:font_awesome_flutter/font_awesome_flutter.dart';

class StartWidget extends StatefulWidget {
  const StartWidget({Key? key}) : super(key: key);

  @override
  State<StartWidget> createState() => _StartWidgetState();
}

class _StartWidgetState extends State<StartWidget> {
  late TextEditingController _textController;
  late FocusNode _textFieldFocusNode;
  late FocusNode _unfocusNode;

  @override
  void initState() {
    super.initState();
    _textController = TextEditingController();
    _textFieldFocusNode = FocusNode();
    _unfocusNode = FocusNode();
    WidgetsBinding.instance!.addPostFrameCallback((_) => setState(() {}));
  }

  @override
  void dispose() {
    _textController.dispose();
    _textFieldFocusNode.dispose();
    _unfocusNode.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return GestureDetector(
      onTap: () => _unfocusNode.canRequestFocus
          ? FocusScope.of(context).requestFocus(_unfocusNode)
          : FocusScope.of(context).unfocus(),
      child: Scaffold(
        backgroundColor: Colors.white,
        body: SafeArea(
          top: true,
          child: Column(
            mainAxisSize: MainAxisSize.max,
            children: [
              Container(
                width: double.infinity,
                height: 199,
                color: Colors.blue, // Replace with your primary color
                child: Column(
                  mainAxisAlignment: MainAxisAlignment.center,
                  children: [
                    Row(
                      mainAxisAlignment: MainAxisAlignment.spaceBetween,
                      children: [
                        ElevatedButton(
                          onPressed: () async {
                            // Your action for camera start
                            // ask user permission to acces camera
                            // if permission granted then start camera  else show error
                            // open camera and diplay feed on screen
                            // start taking frames, one in every 5 second. Display it in a small window(a snip of each frame), then convert to byte stream and include it to the client request
                            // if the hardcoded prompt is not changed, make an api call to the model(gemini pro vision)
                            //Receive output from the model after api call and display it on the output window as well as in speech form
                            // proceed until the stop button is pressed
                          },
                          style: ElevatedButton.styleFrom(
                            primary:
                                Colors.blue, // Replace with your primary color
                            padding: EdgeInsets.zero,
                            elevation: 0,
                          ),
                          child: FaIcon(
                            FontAwesomeIcons.camera,
                            color: Colors
                                .white, // Replace with your secondary color
                          ),
                        ),
                        ElevatedButton(
                          onPressed: () async {
                            // Your action for camera stop
                          },
                          style: ElevatedButton.styleFrom(
                            primary:
                                Colors.blue, // Replace with your primary color
                            padding: EdgeInsets.zero,
                            elevation: 0,
                          ),
                          child: Icon(
                            Icons.stop_circle,
                            color: Colors.red, // Replace with your error color
                            size: 15,
                          ),
                        ),
                      ],
                    ),
                  ],
                ),
              ),
              Expanded(
                child: Container(
                  color: Colors.grey[200], // Replace with your background color
                  child: Column(
                    mainAxisAlignment: MainAxisAlignment.center,
                    children: [
                      Container(
                        width: 400,
                        height: 200,
                        color:
                            Colors.white, // Replace with your background color
                        child: Padding(
                          padding: EdgeInsets.all(25),
                          child: Text(
                            'Model Text Output...',
                            style: TextStyle(fontSize: 18),
                          ),
                        ),
                      ),
                      ElevatedButton(
                        onPressed: () {
                          print('Button pressed ...');
                        },
                        style: ElevatedButton.styleFrom(
                          primary:
                              Colors.blue, // Replace with your primary color
                          padding: EdgeInsets.symmetric(horizontal: 24),
                          elevation: 3,
                          shape: RoundedRectangleBorder(
                            borderRadius: BorderRadius.circular(8),
                          ),
                        ),
                        child: Text(
                          'Play',
                          style: TextStyle(fontSize: 16),
                        ),
                      ),
                    ],
                  ),
                ),
              ),
              Padding(
                padding: EdgeInsets.all(8),
                child: Row(
                  children: [
                    Expanded(
                      child: TextFormField(
                        controller: _textController,
                        focusNode: _textFieldFocusNode,
                        autofocus: true,
                        obscureText: false,
                        decoration: InputDecoration(
                          labelText: 'Enter Prompt',
                          hintText: 'Prompt...',
                          enabledBorder: OutlineInputBorder(
                            borderSide: BorderSide(
                              color: Colors
                                  .blue, // Replace with your secondary color
                              width: 2,
                            ),
                            borderRadius: BorderRadius.circular(8),
                          ),
                          focusedBorder: OutlineInputBorder(
                            borderSide: BorderSide(
                              color: Colors
                                  .blue, // Replace with your primary color
                              width: 2,
                            ),
                            borderRadius: BorderRadius.circular(8),
                          ),
                        ),
                        style: TextStyle(fontSize: 16),
                        maxLines: 2,
                        validator: (value) {
                          // Your validation logic here
                        },
                      ),
                    ),
                    Padding(
                      padding: EdgeInsets.only(left: 5),
                      child: IconButton(
                        color: Colors.blue, // Replace with your primary color
                        icon: Icon(
                          Icons.send_outlined,
                          size: 24,
                        ),
                        onPressed: () {
                          print('IconButton pressed ...');
                        },
                      ),
                    ),
                  ],
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }
}

void main() {
  runApp(MaterialApp(
    home: StartWidget(),
  ));
}
