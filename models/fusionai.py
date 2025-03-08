import g4f
import json

def generate_response(prompt):
    try:
        # panggil api g4f untuk mendapatkan response
        response = g4f.ChatCompletion.create(
            model="o3-mini",
            provider=g4f.Provider.Blackbox,  # pilih provider yang didukung
            messages=[
                {"role": "system", "content": ""},
                {"role": "user", "content": prompt},
            ],
        )

        print("raw response:", response)  # debug: lihat response asli

        # jika response berupa string, coba parse sebagai json
        if isinstance(response, str):
            try:
                response = json.loads(response)
            except json.JSONDecodeError:
                return {"response": response}  # anggap response itu teks biasa

        # pastikan response adalah dict dan memiliki key 'choices'
        if isinstance(response, dict) and "choices" in response:
            choices = response["choices"]
            if isinstance(choices, list) and choices:
                first_choice = choices[0]
                if isinstance(first_choice, dict) and "message" in first_choice and "content" in first_choice["message"]:
                    return {"response": first_choice["message"]["content"]}
                else:
                    return {"response": "error: key 'message' atau 'content' tidak ditemukan di response"}
            else:
                return {"response": "error: 'choices' kosong atau tidak berbentuk list"}
        else:
            return {"response": "error: format response tidak sesuai, tidak ada key 'choices'"}

    except Exception as e:
        return {"response": f"error: exception saat memproses response: {str(e)}"}
      
