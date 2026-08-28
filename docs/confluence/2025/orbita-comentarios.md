# Órbita - Comentários

> Fonte: https://farmarcas.atlassian.net/wiki/spaces/SR/pages/3200450582/rbita+-+Coment+rios · Última atualização no Confluence: abr. 03, 2025

### **Permitir a edição de um comentário**

‌

**Regras gerais:**

* Em reunião com a área, alinhamos que apenas o próprio autor do comentário deve conseguir editar ou excluir um comentário.
* Alinhamos que o campo de comentários deve ter uma limitação de 500 caracteres e devemos incluir essa contagem na tela.
* Teremos a opção de inclusão de anexos em um comentário.
* A inclusão de anexos deve estar limitada a 50MB no total dos arquivos.

‌

1. **Exibição da opção de edição**

    * Apenas o autor do comentário pode editar o próprio comentário, 
    * Quando eu clicar no ícone de **três pontos** ao lado do comentário, a opção de edição deve aparecer.
    * Caso eu seja um usuário diferente do dono do comentário, deve ser exibido um bloqueio nos **três pontos** ao passar o mouse;
    * Não devo conseguir acessar as opções, visto que ficará com um **ícone de proibido.**
    
2. **Abertura do modo de edição**

    * Dado que selecionei a opção **"Editar Comentário"**,
    * Quando o modo de edição for ativado,
    * Então o campo do comentário deve ser editável, mantendo o conteúdo original preenchido.
    * E deve haver as opções **"Cancelar"** e **"Salvar Comentário"**.
    
3. **Edição do comentário**

    * Dado que estou no modo de edição,
    * Quando eu modificar o conteúdo do comentário,
    * Então o botão **"Salvar Comentário"** deve estar habilitado.
    * E, caso eu clique em **"Cancelar"**, a edição deve ser descartada e o comentário deve voltar ao estado original.
    
4. **Salvar o comentário atualizado**

    * Dado que alterei o comentário e cliquei em **"Salvar Comentário"**,
    * Quando a atualização for bem-sucedida,
    * Então o sistema deve exibir a versão atualizada do comentário.
    * E deve exibir um aviso visual confirmando a atualização bem-sucedida.
    
5. **Manutenção de anexos**

    * Dado que meu comentário possui arquivos anexados,
    * Quando eu editar apenas o texto sem remover os anexos,
    * Então os arquivos anexados devem ser mantidos.
    
6. **Registro da edição**

    * Dado que editei o meu comentário,
    * Quando a edição for salva,
    * Então o sistema deve indicar que o comentário foi **editado**, exibindo o nome do usuário, a data e hora da edição. **(será exibido onde já temos o histórico, ao lado direito da tela)**
    

 

**Notas Técnicas:**

* Apenas o autor do comentário pode editá-lo.
* O botão **"Salvar Comentário"** deve ficar desabilitado caso não haja alterações.
* Deve haver um limite de **500 caracteres** para o campo de edição.

‌

### **Permitir a exclusão de um comentário**

‌

1. **Exibição da opção de exclusão**

    * Dado que sou o autor do comentário,
    * Quando eu clicar no ícone de **três pontos** ao lado do meu comentário,
    * Então devo visualizar a opção **"Excluir Comentário"** no menu suspenso.
    * Dado que não sou o autor do comentário,
    * Quando eu passar o **mouse sobre os três pontinhos,**
    * Não devo conseguir acessar as opções, visto que ficará com um **ícone de proibido.**
    
2. **Confirmação antes da exclusão**

    * Dado que cliquei na opção **"Excluir Comentário"**,
    * Quando o sistema exibir um alerta **(modal)** de confirmação,
    * Então devo ter as opções de **excluir** ou **cancelar** a exclusão.
    
3. **Remoção definitiva do comentário**

    * Dado que confirmei a exclusão do comentário,
    * Quando a ação for processada com sucesso,
    * Então o comentário deve ser removido da interface e não deve mais ser visível para os usuários.
    
4. **Cancelar a exclusão antes da confirmação**

    * Dado que cliquei na opção de excluir um comentário,
    * Quando eu escolher a opção **"Cancelar"** na mensagem de confirmação,
    * Então a exclusão não deve ser realizada e o comentário deve permanecer visível.
    
5. **Remoção de anexos vinculados ao comentário**

    * Dado que excluí um comentário que possuía anexos,
    * Quando a exclusão for concluída,
    * Então todos os arquivos anexados ao comentário também devem ser removidos do sistema.
    
6. **Mensagem de sucesso**

    * Dado que excluí um comentário,
    * Quando a exclusão for concluída,
    * Então o sistema deve exibir uma mensagem confirmando que o comentário foi removido com sucesso.
    

**Notas Técnicas:**

* Apenas o autor do comentário pode excluí-lo.
* A exclusão deve ser definitiva e não permitir recuperação.
* Caso ocorra um erro ao excluir, o sistema deve exibir uma mensagem informando o problema.

‌

### **Inclusão de Anexo em Comentários**

‌

1. **Inclusão de anexo**

    * Dado que estou escrevendo ou editando um comentário,
    * Quando eu clicar na opção de **anexar arquivos**,
    * Então devo poder selecionar,
    * E os arquivos selecionados devem ser exibidos visualmente abaixo do campo de comentário.
    
2. **Restrição de formato e tamanho**

    * Dado que estou anexando um arquivo,
    * Quando o arquivo selecionado for de um tamanho não permitido **(até 50mb)**,
    * Então o sistema deve exibir uma mensagem informando os formatos suportados e o tamanho máximo permitido.
    
3. **Visualização do progresso de upload**

    * Dado que selecionei um ou mais arquivos,
    * Quando o upload estiver em andamento,
    * Então o sistema deve exibir uma barra de progresso ou um indicador de carregamento.
    * E, caso o upload falhe, deve ser exibida uma mensagem informando o erro.
    
4. **Salvar comentário com anexo**

    * Dado que adicionei um ou mais anexos,
    * Quando eu clicar em **"Salvar Comentário"**,
    * Então o comentário deve ser salvo com os arquivos anexados e exibidos corretamente na interface.
    
5. **Salvar anexo sem nenhum comentário**

    * Dado que adicionei um anexo sem nenhum comentário,
    * O próprio anexo deve ser considerado como um comentário,
    * Então o sistema deve registar o **nome do usuário, data e horário em que foi incluído.**
    

**Notas Técnicas:**

* Apenas o autor do comentário pode adicionar anexos a um comentário salvo anteriormente.
* O sistema deve validar os formatos e tamanhos antes de iniciar o upload.
* Deve haver um limite de quantidade e tamanho total dos arquivos anexados.
* Tanto um comentário pode ser adicionado sem anexos, quanto um anexo pode ser adicionado sem um comentário.

‌

### **Exclusão de Anexos em Comentários**

‌

1. **Exibição da opção de remoção de anexo**

    * Dado que estou editando um comentário com anexos,
    * Quando os arquivos anexados forem exibidos,
    * Então cada anexo deve ter uma opção para **removê-lo** **(um ícone de lixeira).**
    
2. **Remoção de anexo antes de salvar**

    * Dado que estou no modo de **edição,**
    * Quando eu clicar na opção de **excluir um anexo (um ícone de lixeira),**
    * Então o anexo deve ser removido da lista de anexos antes de eu salvar o comentário.
    
3. **Confirmar remoção após salvar**

    * Dado que removi um anexo durante a edição,
    * Quando eu clicar em **"Salvar Comentário"**,
    * Então o anexo não deve mais ser exibido no comentário publicado.
    
4. **Cancelar remoção antes de salvar**

    * Dado que estou editando um comentário e removi um anexo,
    * Quando eu clicar em **"Cancelar"**,
    * Então a edição deve ser descartada e o anexo original **deve permanecer no comentário.**
    

**Notas Técnicas:**

* Apenas o autor do comentário pode excluir anexos.
* A exclusão do anexo só deve ficar disponível quando o usuário clicar na edição.
* A remoção do anexo só deve ser efetivada após o usuário salvar a edição.
* Se um anexo for removido, não deve haver referência a ele no banco de dados ou na interface.

‌
