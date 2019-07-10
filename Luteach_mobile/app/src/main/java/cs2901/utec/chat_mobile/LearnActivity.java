package cs2901.utec.chat_mobile;

import android.app.Activity;
import android.content.Intent;
import android.os.Bundle;
import android.support.v7.app.AppCompatActivity;
import android.view.View;
import android.widget.EditText;

import com.android.volley.Request;
import com.android.volley.RequestQueue;
import com.android.volley.Response;
import com.android.volley.VolleyError;
import com.android.volley.toolbox.JsonObjectRequest;
import com.android.volley.toolbox.Volley;

import org.json.JSONObject;

import java.util.HashMap;
import java.util.Map;

public class LearnActivity extends AppCompatActivity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_learn);
    }

    public Activity getActivity(){
        return this;
    }


    public void ClickSend(View v) {
        postLearn();
        Intent intent = new Intent(getActivity(), MenuActivity.class);
        intent.putExtra("user_id", getIntent().getExtras().get("user_id").toString());
        intent.putExtra("username", getIntent().getExtras().get("username").toString());
        startActivity(intent);
    }

    public void postLearn(){
        String url = "http://10.0.2.2:5000/postLearn";
        RequestQueue queue = Volley.newRequestQueue(this);
        Map<String, String> params = new HashMap();
        final String user_from_id = getIntent().getExtras().get("user_id").toString();
        final String user_from_name = getIntent().getExtras().get("username").toString();
        final String Tema = ((EditText)findViewById(R.id.txtTema)).getText().toString();
        final String Curso = ((EditText)findViewById(R.id.txtCurso)).getText().toString();
        final String Lugar = ((EditText)findViewById(R.id.txtLugar)).getText().toString();
        final String Hora = ((EditText)findViewById(R.id.txtHora)).getText().toString();
        final String Tiempo = ((EditText)findViewById(R.id.txtTiempo)).getText().toString();
        params.put("user_from_id", user_from_id);
        params.put("user_from_name", user_from_name);
        params.put("tema", Tema);
        params.put("curso", Curso);
        params.put("lugar", Lugar);
        params.put("hora", Hora);
        params.put("tiempo", Tiempo);
        JSONObject parameters = new JSONObject(params);
        JsonObjectRequest jsonObjectRequest = new JsonObjectRequest(
                Request.Method.POST,
                url,
                parameters,
                new Response.Listener<JSONObject>() {
                    @Override
                    public void onResponse(JSONObject response) {
                        // TODO
                    }
                }, new Response.ErrorListener() {

            @Override
            public void onErrorResponse(VolleyError error) {
                // TODO: Handle error
                error.printStackTrace();
            }
        });
        queue.add(jsonObjectRequest);
    }
}
