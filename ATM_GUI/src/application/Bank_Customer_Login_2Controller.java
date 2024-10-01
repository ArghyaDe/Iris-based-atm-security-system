//Iris Scanning page for customer
package application;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import javafx.event.ActionEvent;
import javafx.fxml.FXML;
import javafx.fxml.FXMLLoader;
import javafx.scene.Node;
import javafx.scene.Parent;
import javafx.scene.Scene;
import javafx.scene.control.Button;
import javafx.scene.control.Label;
import javafx.stage.Stage;

public class Bank_Customer_Login_2Controller {
	@FXML
	private Label label;

	@FXML
	private Button loginOption;

	private String Name,UserId,UserName,email,Bank[]=new String[]{" "," "," "," "," "},AccountNo[]=new String[]{" "," "," "," "," "};
	
	private int NoBank;

	public void loginOption(final ActionEvent event) {

	}

	public void setDisebleButton(boolean vis){
		loginOption.setDisable(vis);
	}

	public void loginIris(ActionEvent event) {
		boolean k = false;
		try {
			k = IrisRecognition();
		} catch (final IOException e) {
			// TODO Auto-generated catch block
			System.out.print(e);
		}
		if (k==true) {
			try {
	            FXMLLoader loader=new FXMLLoader(getClass().getResource("IrisMatched.fxml"));
				Parent root = (Parent)loader.load();
				Stage window = (Stage)((Node)event.getSource()).getScene().getWindow();	// It  is used to get Window information
				IrisMatchedController irisMatchedController=loader.getController();
				irisMatchedController.setAll(Name, UserName, UserId,email,Bank,AccountNo);
				Scene scene = new Scene(root);
				window.setScene(scene);
				window.setFullScreen(true);
				window.show();
	        } catch (Exception e) {
	            //TODO: handle exception
	        	System.out.print(e);
	        }
		}else{
			try {
	            Parent root = FXMLLoader.load(getClass().getResource("IrisUnmatched.fxml")); 
	            Stage window = (Stage)((Node)event.getSource()).getScene().getWindow();	// It  is used to get Window information
	            Scene scene = new Scene(root);
	            window.setScene(scene);
	            window.setFullScreen(true);
	            window.show();
	        } catch (Exception e) {
	            //TODO: handle exception
	        	System.out.print(e);
	        }
		}
	}

	private boolean IrisRecognition() throws IOException{
		boolean t = false;
		final String command[]={"python","RealtimeIrisDetect.py"};
        final ProcessBuilder pd = new ProcessBuilder(command);
		final Process p = pd.start();
		final BufferedReader br = new BufferedReader(new InputStreamReader(p.getInputStream()));
		String line;
		try {
			line = br.readLine();
			if (line!=null) {
                if(line.equals("success")){
					Name=new String(br.readLine());
					UserId=new String(br.readLine());
					UserName=new String(br.readLine());
					NoBank=Integer.parseInt(new String(br.readLine()));
					email=new String(br.readLine());
					for (int i=0;i<NoBank;i++) {
						Bank[i]=new String(br.readLine());
						AccountNo[i]=new String(br.readLine());
					}
					t=true;
				}
            }
		} catch (final Exception e) {
			System.out.println(e);
		}
		return t;
	}

}
