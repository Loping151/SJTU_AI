#coding=utf8
import torch
import torch.nn as nn
import torch.nn.utils.rnn as rnn_utils


class SLUTagging(nn.Module):

    def __init__(self, config):
        super(SLUTagging, self).__init__()
        self.config = config
        self.cell = config.encoder_cell
        self.word_embed = nn.Embedding(config.vocab_size, config.embed_size, padding_idx=0)
        self.rnn_in = getattr(nn, self.cell)(config.embed_size, config.hidden_size // 2, num_layers=config.num_layer, bidirectional=True, batch_first=True)
        self.rnn_mem = getattr(nn, self.cell)(config.embed_size, config.hidden_size // 2, num_layers=config.num_layer, bidirectional=True, batch_first=True)
        self.dropout_layer = nn.Dropout(p=config.dropout)
        self.loss_fct = nn.CrossEntropyLoss(ignore_index=config.tag_pad_idx)
        #self.output_layer = TaggingFNNDecoder(config.hidden_size, config.num_tags, config.tag_pad_idx)
        self.output_layer = nn.Linear(config.hidden_size, config.num_tags)
        self.test_layer1 = nn.Linear(config.hidden_size, config.hidden_size)
        self.test_layer2 = nn.Linear(config.embed_size, config.hidden_size)



    def forward(self, batch):
        
        tag_ids = batch.tag_ids
        tag_mask = batch.tag_mask
        input_ids = batch.input_ids
        word_lengths = batch.word_lengths
        max_word_lenth = batch.max_word_lenth
        max_seq_lenth = batch.max_seq_lenth
        batch_size = tag_ids.shape[0]

        #torch.autograd.set_detect_anomaly(True)
        result = torch.zeros((batch_size,max_seq_lenth,max_word_lenth,self.config.num_tags),device = tag_ids.device)
        mem = torch.zeros((batch_size,max_seq_lenth,max_word_lenth,self.config.hidden_size),device = tag_ids.device)
        #current = torch.zeros((tag_ids.shape[0],max_word_lenth,self.config.embed_size),device = tag_ids.device)
        for i in range(max_seq_lenth):            
            #if i == 1:
            #mem = embed.clone()
            current_input_ids = input_ids[:,i,:]
            embed = self.word_embed(current_input_ids)

            #mem = self.test_layer2(mem)
            #current = embed
            #mem = embed
            # attention_weights_tmp = torch.bmm(mem, current.transpose(1,2))
            # attention_weights = torch.softmax(attention_weights_tmp, dim=-1)
            # attended_context = torch.bmm(attention_weights, current)    
            packed_inputs = rnn_utils.pack_padded_sequence(embed, word_lengths[:,i], batch_first=True, enforce_sorted=False)
            packed_rnn_out_mem, h_t_c_t_mem = self.rnn_mem(packed_inputs)  # bsize x seqlen x dim
            rnn_out_mem, unpacked_len_mem = rnn_utils.pad_packed_sequence(packed_rnn_out_mem, batch_first=True)
            hiddens_mem = self.dropout_layer(rnn_out_mem)
            mem[:,i,0:hiddens_mem.shape[1],:] = hiddens_mem.clone()
            packed_rnn_out, h_t_c_t = self.rnn_in(packed_inputs)  # bsize x seqlen x dim
            rnn_out, unpacked_len = rnn_utils.pad_packed_sequence(packed_rnn_out, batch_first=True)
            hiddens = self.dropout_layer(rnn_out)
            hiddens_pad = torch.zeros((batch_size,max_word_lenth,self.config.hidden_size),device=input_ids.device)
            hiddens_pad[:,0:hiddens.shape[1],:] = hiddens
            #print(hiddens.shape)
            #print(mem[:,0:i+1,:,:].reshape(batch_size,i+1,-1).shape,hiddens_pad.transpose(1,2).reshape(batch_size,-1,1).shape)
            t1 = mem[:,0:i+1,:,:].reshape(batch_size,i+1,-1).clone()
            #hiddens_pad_mem = torch.zeros((batch_size,max_word_lenth,self.config.hidden_size),device=input_ids.device)
           # hiddens_pad_mem[:,0:hiddens.shape[1],:] = hiddens_mem
            #t1 = hiddens_pad_mem.reshape(batch_size,1,-1)
            t2 = hiddens_pad.transpose(1,2).reshape(batch_size,-1,1)
            temp1 = torch.bmm(t1,t2)
            
            weights = torch.softmax(temp1, dim=-1)
            #print(weights.shape,hiddens.shape)
            weighted_sum = torch.sum(weights.reshape(batch_size,1,1,i+1).repeat(1,max_word_lenth,self.config.hidden_size,1) * hiddens_pad[:,:,:,None].repeat(1,1,1,i+1),dim=-1)
            temp_sum = weighted_sum + hiddens_pad
            temp_sum = self.dropout_layer(self.test_layer1(temp_sum))
            final_feature = temp_sum + self.test_layer2(embed)
            #current[:,0:hiddens.shape[1],:] = hiddens
            #print(mem.shape,current.shape)
            #mem = self.test_layer(mem)
            #concat = torch.cat((current,mem),dim=-1)
            tag_output = self.output_layer(final_feature)
            result[:,i,0:tag_output.shape[1],:] = tag_output
            #mem[:,0:rnn_out.shape[1],:] = rnn_out
            #mem = current.clone()

        
        result += (1 - tag_mask).unsqueeze(-1).repeat(1, 1, 1,self.config.num_tags) * -1e32
        prob = torch.softmax(result, dim=-1)
        
        if tag_ids is not None:
            loss = self.loss_fct(result.reshape(-1, result.shape[-1]), tag_ids.reshape(-1))
            return prob, loss
        return (prob, )
             

    def decode(self, label_vocab, batch):
        batch_size = len(batch)
        labels = batch.labels
        output = self.forward(batch)
        prob = output[0]
        predictions = []
        finbal_labels = []
        for i in range(batch_size):
            for j in range(batch.seq_lengths[i]):
                pred = torch.argmax(prob[i][j], dim=-1).cpu().tolist()
                pred_tuple = []
                idx_buff, tag_buff, pred_tags = [], [], []
                pred = pred[:len(batch.utt[i][j])]
                for idx, tid in enumerate(pred):
                    tag = label_vocab.convert_idx_to_tag(tid)
                    pred_tags.append(tag)
                    if (tag == 'O' or tag.startswith('B')) and len(tag_buff) > 0:
                        slot = '-'.join(tag_buff[0].split('-')[1:])
                        value = ''.join([batch.utt[i][j][q] for q in idx_buff])
                        idx_buff, tag_buff = [], []
                        pred_tuple.append(f'{slot}-{value}')
                        if tag.startswith('B'):
                            idx_buff.append(idx)
                            tag_buff.append(tag)
                    elif tag.startswith('I') or tag.startswith('B'):
                        idx_buff.append(idx)
                        tag_buff.append(tag)
                if len(tag_buff) > 0:
                    slot = '-'.join(tag_buff[0].split('-')[1:])
                    value = ''.join([batch.utt[i][j][q] for q in idx_buff])
                    pred_tuple.append(f'{slot}-{value}')
                predictions.append(pred_tuple)
                
                if not (labels is None):
                    finbal_labels.append(labels[i][j])
                
                
        if len(output) == 1:
            return predictions
        else:
            loss = output[1]
            return predictions, finbal_labels, loss.cpu().item()



