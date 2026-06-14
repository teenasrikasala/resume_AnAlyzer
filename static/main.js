let atsChart=null;
const form=document.querySelector('form');
const atsscore=document.getElementById('ats-score');
const skills_matching=document.getElementById('skills-matching');
const missingskills=document.getElementById('missing-skills');
const suggestions=document.getElementById('suggestions')
const summary=document.getElementById('summary');
form.addEventListener('submit' ,async function(event){
event.preventDefault(); 
const formdata=new FormData(form);        
atsscore.innerHTML='🔄️Analyzinggg...'
skills_matching.innerHTML=''
missingskills.innerHTML=''
suggestions.innerHTML=''
summary.textContent=''
try{
    const response=await fetch('/analyze',{
           method:"POST",
           body:formdata
          });
    const result=await response.json();
     if(atsChart){
        atsChart.destroy();
     }
    atsChart=new Chart(
        document.getElementById('ats-chart'),{
        type:"doughnut",
        data:{
            labels:["Matched","Remaining"],
            datasets:[
                {
                data:[
                    result.atsscore,
                    100-result.atsscore
                ],
                 backgroundColor:
                 [
                     "#22c55e",
                     "#e5e7eb"
               ]
            }
        ]
        }
        }
    );
    result.skills_matching.forEach(skill => {
        const li=document.createElement('li');
        li.textContent='✅'+skill;
        skills_matching.appendChild(li);
    });
    result.missingskills.forEach(skill=>{
            const li=document.createElement('li');
            li.textContent='❌'+skill;
            missingskills.appendChild(li);
    });
    result.suggestions.forEach(item=>{
        const li=document.createElement('li');
        li.textContent='💡'+item;
        suggestions.appendChild(li);
    });
    atsscore.textContent = result.atsscore + "%";
    summary.textContent=result.summary;
}
catch(error){
    atsscore.textContent='Error in data analyzing';
    console.error(error);
}});