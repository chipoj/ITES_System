function toggleFields() {
    var radioValue = document.querySelector('input[name="choice"]:checked').value;
    var fieldID1 = document.getElementById('referenceID1');
    var fieldID2 = document.getElementById('referenceID2');
    var fieldID3 = document.getElementById('referenceID3');
    var fieldID4 = document.getElementById('referenceID4');
    var fieldID5 = document.getElementById('referenceID5');
    var fieldID6 = document.getElementById('referenceID6');
    var fieldID7 = document.getElementById('referenceID7');
    var fieldID8 = document.getElementById('referenceID8');
    var fieldID9 = document.getElementById('referenceID9');
    var fieldID10 = document.getElementById('referenceID10');

    // var inputElement = document.getElementById('my-input');
    // inputElement.value = '';

    if (radioValue === 'option1') {
      fieldID1.style.display = 'block';
      fieldID2.style.display = 'block';
      fieldID3.style.display = 'none';
      fieldID4.style.display = 'none';
      fieldID4.value = '';
      fieldID5.style.display = 'none';
      fieldID6.style.display = 'none';
      fieldID6.value = '';
      fieldID7.style.display = 'none';
      fieldID8.style.display = 'none';
      fieldID8.value = '';
      fieldID9.style.display = 'none';
      fieldID10.style.display = 'none';
      fieldID10.value = '';
     

    } else if (radioValue === 'option2') {
      fieldID1.style.display = 'none';
      fieldID2.style.display = 'none';
      fieldID2.value = '';
      fieldID3.style.display = 'block';
      fieldID4.style.display = 'block';
      fieldID5.style.display = 'block';
      fieldID6.style.display = 'block';
      fieldID7.style.display = 'block';
      fieldID8.style.display = 'block';
      fieldID9.style.display = 'block';
      fieldID10.style.display = 'block';
    } else {
      fieldID1.style.display = 'none';
      fieldID2.style.display = 'none';
      fieldID2.style.display = 'none';
      fieldID3.style.display = 'none';
      fieldID4.style.display = 'none';
      fieldID5.style.display = 'none';
      fieldID6.style.display = 'none';
      fieldID7.style.display = 'none';
      fieldID8.style.display = 'none';
      fieldID9.style.display = 'none';
      fieldID10.style.display = 'none';
    }
  }




