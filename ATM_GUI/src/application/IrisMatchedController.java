package application;

import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.net.URL;
import java.util.ResourceBundle;

import javafx.event.ActionEvent;
import javafx.fxml.FXML;
import javafx.fxml.FXMLLoader;
import javafx.fxml.Initializable;
import javafx.scene.Node;
import javafx.scene.Parent;
import javafx.scene.Scene;
import javafx.scene.control.Button;
import javafx.scene.control.Label;
import javafx.scene.image.Image;
import javafx.scene.image.ImageView;
import javafx.scene.text.Text;
import javafx.stage.Stage;

public class IrisMatchedController implements Initializable{
	
	private String UName,UserId,email,Bank[]=new String[]{" "," "," "," "," "},AccountNo[]=new String[]{" "," "," "," "," "};
	@FXML
	private Text txtUserName;
	
	@FXML
	private Label Name;

	@FXML
	private Text txtUserId;

	@FXML
	private ImageView imgClient;

	@FXML
	private Button btnStart;

	@FXML
	public void StartTranscation(ActionEvent event) {
		try {
			FXMLLoader loader=new FXMLLoader(getClass().getResource("TransactionAuthentication.fxml"));
            Parent root = (Parent)loader.load(); 
            Stage window = (Stage)((Node)event.getSource()).getScene().getWindow();	// It  is used to get Window information
            TransactionAuthenticationController transactionAuthenticationController=loader.getController();
            try {
            	transactionAuthenticationController.setAll(this.UName,this.UserId,this.email,this.Bank,this.AccountNo);
            }
            catch(Exception e) {
            	System.out.println(e);
            }
            Scene scene = new Scene(root);
            window.setScene(scene);
            window.setFullScreen(true);
            window.show();
        } catch (Exception e) {
            //TODO: handle exception
        	System.out.print(e);
        }
	}

	public void setAll(String SName,String StxtUserName,String StxtUserId,String email,String Bank[],String Account[]){
		Name.setText(SName);
		this.UName=new String(SName);
		this.UserId=new String(StxtUserId);
		txtUserId.setText(this.UserId);
		this.email=new String(email);
		for (int i=0;i<Bank.length;i++) {
			this.Bank[i]=Bank[i];
			this.AccountNo[i]=Account[i];
		}
		txtUserName.setText(this.UName);
	}

	@Override
	public void initialize(URL arg0, ResourceBundle arg1) {
		// TODO Auto-generated method stub
		FileInputStream filein;
		try {
			filein = new FileInputStream("temp.jpg");
			imgClient.setImage(new Image(filein));
		} catch (FileNotFoundException e) {
			// TODO Auto-generated catch block
			System.out.print(e);
		}
	}

}
