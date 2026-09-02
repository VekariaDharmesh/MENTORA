with open("frontend/app.js", "r") as f:
    content = f.read()

old_block = """               if (jobStat.stage === 'VISUAL' || jobStat.stage === 'AVATAR') {
                 if (step4) {
                   step4.className = 'prep-step-item is-done';
                   step4.querySelector('.prep-step-icon').textContent = '✓';
                 }
                 if (step5 && step5.className !== 'prep-step-item is-done') {
                   step5.className = 'prep-step-item is-active';
                   step5.querySelector('.prep-step-icon').textContent = '●';
                 }
               }

               if (jobStat.stage === 'COMPOSE' || jobStat.stage === 'UPLOAD' || jobStat.stage === 'READY') {
                 if (step5) {
                   step5.className = 'prep-step-item is-done';
                   step5.querySelector('.prep-step-icon').textContent = '✓';
                 }
                 if (step6 && step6.className !== 'prep-step-item is-done') {
                   step6.className = 'prep-step-item is-active';
                   step6.querySelector('.prep-step-icon').textContent = '●';
                 }
               }"""

new_block = """               // Update Dynamic Progress Text
               if (step5) {
                   const progressTxt = jobStat.progress > 0 ? ` (${jobStat.progress}%)` : '';
                   const label = step5.querySelector('span');
                   if (label) {
                       label.textContent = `Creating teacher video${progressTxt}`;
                   }
               }

               if (jobStat.stage === 'VIDEO_RENDERING' || jobStat.stage === 'VIDEO_SUBMISSION') {
                 if (step4) {
                   step4.className = 'prep-step-item is-done';
                   step4.querySelector('.prep-step-icon').textContent = '✓';
                 }
                 if (step5 && step5.className !== 'prep-step-item is-done') {
                   step5.className = 'prep-step-item is-active';
                   step5.querySelector('.prep-step-icon').textContent = '●';
                 }
               }

               if (jobStat.stage === 'READY') {
                 if (step5) {
                   step5.className = 'prep-step-item is-done';
                   step5.querySelector('.prep-step-icon').textContent = '✓';
                   const label = step5.querySelector('span');
                   if (label) label.textContent = 'Teacher video created';
                 }
                 if (step6 && step6.className !== 'prep-step-item is-done') {
                   step6.className = 'prep-step-item is-active';
                   step6.querySelector('.prep-step-icon').textContent = '●';
                 }
               }"""

content = content.replace(old_block, new_block)

with open("frontend/app.js", "w") as f:
    f.write(content)
