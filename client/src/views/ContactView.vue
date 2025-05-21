<template>
  <div class="contact">
    <h1>📬 Get in Touch</h1>
    <p class="contact-intro">
      We would love to hear from you, whether you're interested in collaborating, have questions, or want to provide feedback.  
      Please fill out the form below and we will get back to you as soon as we can.
    </p>

    <form
      id="contact-form"
      action="https://formspree.io/f/mwpldkop"
      method="POST"
      @submit.prevent="submitForm"
    >
      <label for="name">Name</label>
      <input type="text" autocomplete="off" id="name" name="name" required placeholder="Enter your name" />

      <label for="email">Email<span class="required">*</span></label>
      <input type="email" autocomplete="off" id="email" name="email" required placeholder="Enter your email" />

      <label for="subject">Subject <span class="required">*</span></label>
      <input type="text" autocomplete="off" id="subject" name="subject" required placeholder="Enter a subject" />

      <label for="message">Message <span class="required">*</span></label>
      <textarea
        id="message"
        name="message"
        autocomplete="off"
        rows="10"
        required
        placeholder="Enter your message"
        @input="updateWordCount"
      ></textarea>
      <small class="word-counter">{{ wordCount }} / 250 words</small>

      <input type="hidden" name="_captcha" value="false" />
      <input type="text" name="_gotcha" style="display: none" />
      <input type="hidden" name="_subject" value="New message from ML Hub contact form" />

      <button type="submit">Send Message</button>

      <div v-if="formSubmitted" class="success-message">
        ✅ Thank you! Your message has been sent.
      </div>
    </form>
  </div>
</template>

<script>
export default {
  props: {
    user: Object
  },
  data() {
    return {
      wordCount: 0,
      formSubmitted: false,
    };
  },
  methods: {
    updateWordCount(event) {
      const words = event.target.value.trim().split(/\s+/).filter(Boolean);
      this.wordCount = Math.min(words.length, 250);
      if (words.length > 250) {
        event.target.value = words.slice(0, 250).join(" ");
      }
    },
    async submitForm() {
      const form = document.getElementById("contact-form");
      const formData = new FormData(form);

      if (this.user && this.user.email) {
        formData.append("user_email", this.user.email);
      }

      try {
        const response = await fetch("https://formspree.io/f/mwpldkop", {
          method: "POST",
          body: formData,
          headers: {
            Accept: "application/json",
          },
        });

        if (response.ok) {
          this.formSubmitted = true;
          form.reset();
          this.wordCount = 0;
          setTimeout(() => {
            this.formSubmitted = false;
          }, 5000);
        } else {
          alert("Something went wrong. Please try again.");
        }
      } catch (err) {
        console.error("Form submission error:", err);
        alert("Failed to send message.");
      }
    }
  }
};
</script>

<style scoped>
.contact {
  max-width: 800px;
  margin: 0 auto;
  padding: 2rem;
}

h1 {
  font-size: 1.5rem;
  margin-bottom: 0.5rem;
}

.contact-intro {
  margin-top: 0.5rem;
  color: #444;
}

label {
  display: block;
  margin-top: 1rem;
  font-weight: bold;
}

input,
textarea {
  width: 100%;
  padding: 0.6rem;
  margin-top: 0.25rem;
  box-sizing: border-box;
}

button {
  margin-top: 1.5rem;
  padding: 0.75rem 1.5rem;
  background-color: #007acc;
  color: white;
  border: none;
  cursor: pointer;
}

button:hover {
  background-color: #005fa3;
}

.word-counter {
  display: block;
  margin-top: 0.25rem;
  font-size: 0.9rem;
  color: #666;
}

.required {
  color: red;
}

.success-message {
  color: green;
  margin-top: 1rem;
}
</style>
