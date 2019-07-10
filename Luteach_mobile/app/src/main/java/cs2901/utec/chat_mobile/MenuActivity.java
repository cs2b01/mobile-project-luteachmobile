package cs2901.utec.chat_mobile;

import android.app.Activity;
import android.content.Intent;
import android.os.Bundle;
import android.support.v7.app.AppCompatActivity;
import android.view.View;

public class MenuActivity extends AppCompatActivity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_menu);
    }

    public Activity getActivity(){
        return this;
    }

    public void InicioClicked(View view) {
        Intent intent = new Intent(getActivity(), InicioActivity.class);
        intent.putExtra("user_id", getIntent().getExtras().get("user_id").toString());
        intent.putExtra("username", getIntent().getExtras().get("username").toString());
        startActivity(intent);
    }
    public void ProfesoresClicked(View view) {
        Intent intent = new Intent(getActivity(), ProfesoresActivity.class);
        intent.putExtra("user_id", getIntent().getExtras().get("user_id").toString());
        intent.putExtra("username", getIntent().getExtras().get("username").toString());
        startActivity(intent);
    }
    public void ClasesClicked(View view) {
        Intent intent = new Intent(getActivity(), ClasesActivity.class);
        intent.putExtra("user_id", getIntent().getExtras().get("user_id").toString());
        intent.putExtra("username", getIntent().getExtras().get("username").toString());
        startActivity(intent);
    }
    public void AboutClicked(View view) {
        Intent intent = new Intent(getActivity(), AboutActivity.class);
        startActivity(intent);
    }
    public void ContactClicked(View view) {
        Intent intent = new Intent(getActivity(), ContactActivity.class);
        startActivity(intent);
    }
    public void ContactsClicked(View view) {
        Intent intent = new Intent(getActivity(), ContactsActivity.class);
        intent.putExtra("user_id", getIntent().getExtras().get("user_id").toString());
        intent.putExtra("username", getIntent().getExtras().get("username").toString());
        startActivity(intent);
    }
}
