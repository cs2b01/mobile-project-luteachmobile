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

public class TeachActivity extends AppCompatActivity {
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_teach);
    }
    public Activity getActivity(){
        return this;
    }

    public void ClickEnviar(View v) {
        postTeach();
        Intent intent = new Intent(getActivity(), MenuActivity.class);
        intent.putExtra("user_id", getIntent().getExtras().get("user_id").toString());
        intent.putExtra("username", getIntent().getExtras().get("username").toString());
        startActivity(intent);
    }

    public void postTeach(){
        String url = "http://10.0.2.2:5000/postTeach";
        RequestQueue queue = Volley.newRequestQueue(this);
        Map<String, String> params = new HashMap();
        final String user_from_id = getIntent().getExtras().get("user_id").toString();
        final String Curso = ((EditText)findViewById(R.id.txtCurso_t)).getText().toString();
        params.put("user_from_id_t", user_from_id);
        params.put("curso_t", Curso);
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
