package cs2901.utec.chat_mobile;

import android.app.Activity;
import android.content.Intent;
import android.os.Bundle;
import android.support.v7.app.AppCompatActivity;
import android.view.View;

public class InicioActivity extends AppCompatActivity {
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_inicio);
    }
    public Activity getActivity(){
        return this;
    }

    public void LearnClicked(View view) {
        Intent intent = new Intent(getActivity(), LearnActivity.class);
        intent.putExtra("user_id", getIntent().getExtras().get("user_id").toString());
        intent.putExtra("username", getIntent().getExtras().get("username").toString());
        startActivity(intent);
    }
    public void TeachClicked(View view) {
        Intent intent = new Intent(getActivity(), TeachActivity.class);
        intent.putExtra("user_id", getIntent().getExtras().get("user_id").toString());
        intent.putExtra("username", getIntent().getExtras().get("username").toString());
        startActivity(intent);
    }
}
